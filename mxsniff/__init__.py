# -*- coding: utf-8 -*-

"""
MX Sniffer identifies common email service providers given an email address or a domain name.
"""

from __future__ import absolute_import
import sys
from six import text_type
from six.moves.urllib.parse import urlparse
from email.utils import parseaddr
import dns.resolver
import tldextract

from ._version import __version__, __version_info__  # NOQA
from .providers import providers

__all__ = ['MXLookupException', 'get_domain', 'mxsniff', 'mxbulksniff']

_value = ()  # Used in WildcardDomainDict as a placeholder


class WildcardDomainDict(object):
    """
    Like a dict, but with custom __getitem__ and __setitem__ to make a nested dictionary
    with wildcard support for domain name mappings.

    >>> d = WildcardDomainDict()
    >>> d
    WildcardDomainDict({})
    >>> d['*.example.com'] = 'example-wildcard'
    >>> d['*.wildcard.example.com.'] = 'example-subdotted'
    >>> d['example.com'] = 'example'
    >>> d['www.example.com'] = 'example-www'
    >>> d['example.com']
    'example'
    >>> d['www.example.com']
    'example-www'
    >>> d['wildcard.example.com']
    'example-wildcard'
    >>> d['sub.wildcard.example.com']
    'example-subdotted'
    """
    def __init__(self, *args, **kwargs):
        self.tree = dict(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__ + '(' + repr(self.tree) + ')'

    def _makeparts(self, key):
        parts = key.lower().split('.')
        while '' in parts:
            parts.remove('')  # Handle trailing dot
        return parts[::-1]

    def __setitem__(self, key, value):
        parts = self._makeparts(key)
        tree = self.tree
        for item in parts:
            if item not in tree:
                tree[item] = {}
            tree = tree[item]
        tree[_value] = value

    def __getitem__(self, key):
        parts = self._makeparts(key)
        length = len(parts)
        tree = self.tree
        for counter, item in enumerate(parts):
            last = counter == length - 1
            if item in tree and (not last or last and _value in tree[item]):
                tree = tree[item]
            elif '*' in tree:
                tree = tree['*']
        if _value in tree:
            return tree[_value]
        else:
            raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


provider_domains = WildcardDomainDict()

for name, data in providers.items():
    for domain in data['mx']:
        provider_domains[domain] = name
del name, data, domain


class MXLookupException(Exception):
    pass


def get_domain(email_or_domain):
    """
    Extract domain name from an email address, URL or (raw) domain name.

    >>> get_domain('example@example.com')
    'example.com'
    >>> get_domain('http://www.example.com')
    'example.com'
    >>> get_domain('example.com')
    'example.com'
    """
    if '@' in email_or_domain:
        # Appears to be an email address.
        name, addr = parseaddr(email_or_domain)
        domain = addr.split('@', 1)[-1]
    elif '//' in email_or_domain:
        domain = tldextract.extract(urlparse(email_or_domain).netloc.split(':')[0]).registered_domain
    else:
        domain = email_or_domain.strip()
    return domain


def mxsniff(email_or_domain, ignore_errors=False, cache=None):
    """
    Lookup MX records for a given email address, URL or domain name and identify the email service provider(s)
    from an internal list of known service providers.

    :param str email_or_domain: Email, domain or URL to lookup
    :return: Identified service provider, or a list if there's more than one (in unusual circumstances)

    >>> mxsniff('example.com')['match']
    ['nomx']
    >>> mxsniff('__invalid_domain_name__.com')['match']
    ['nomx']
    >>> mxsniff('example@gmail.com')['match']
    ['google-gmail']
    >>> sorted(mxsniff('https://google.com/').items())
    [('domain', 'google.com'), ('match', ['google-apps']), ('mx', [(10, 'aspmx.l.google.com'), (20, 'alt1.aspmx.l.google.com'), (30, 'alt2.aspmx.l.google.com'), (40, 'alt3.aspmx.l.google.com'), (50, 'alt4.aspmx.l.google.com')]), ('mx_tld', ['google.com']), ('query', 'https://google.com/')]
    """
    domain = get_domain(email_or_domain)
    if cache and domain in cache:
        return cache[domain]

    result = []
    tld = []

    try:
        answers = []  # Default value in case of verbose mode where an error occurs
        answers = sorted([(rdata.preference, rdata.exchange.to_text(omit_final_dot=True).lower())
            for rdata in dns.resolver.query(domain, 'MX')])
        for preference, exchange in answers:
            rdomain = tldextract.extract(exchange).registered_domain
            if rdomain not in tld:
                tld.append(rdomain)
            provider = provider_domains.get(exchange)
            if provider and provider not in result:
                result.append(provider)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        pass
    except dns.exception.DNSException as e:
        if ignore_errors:
            pass
        else:
            raise MXLookupException('{exc} {error} ({domain})'.format(
                exc=e.__class__.__name__, error=text_type(e), domain=domain))

    if not result:
        # Check for self-hosted email servers; identify them with the label 'self'
        if tldextract.extract(domain).registered_domain in tld:
            result.append('self')
        if not result:
            if answers:
                result.append('unknown')  # We don't know this one's provider
            else:
                result.append('nomx')  # This domain has no mail servers

    result = {'query': email_or_domain, 'domain': domain, 'match': result, 'mx': answers, 'mx_tld': tld}
    if cache:
        cache[domain] = result
    return result


def mxbulksniff(items, ignore_errors=True):
    """
    Identify the email service provider of a large set of domains or emails, caching to avoid
    repeat queries. Returns a generator that yields one item at a time

    >>> [(i['query'], i['match']) for i in mxbulksniff(['example.com', 'google.com', 'http://www.google.com'])]
    [('example.com', ['nomx']), ('google.com', ['google-apps']), ('http://www.google.com', ['google-apps'])]
    """
    cache = {}
    for i in items:
        yield mxsniff(i, ignore_errors, cache)


def multiprocess_mxsniff(email_or_domain, ignore_errors=True):
    """
    mxsniff wrapper that converts a KeyboardInterrupt into an Exception. Required because
    of Python bug #8296: http://bugs.python.org/issue8296
    """
    try:
        return mxsniff(email_or_domain, ignore_errors)
    except KeyboardInterrupt:
        raise Exception("KeyboardInterrupt")


def main_internal(args, name='mxsniff'):
    """
    Console script

    >>> main_internal(['example@gmail.com'])
    example@gmail.com: google-gmail
    """
    import argparse
    import json
    from multiprocessing import Pool

    parser = argparse.ArgumentParser(
        prog=name,
        description="Identify email service providers given an email address, URL or domain name",
        fromfile_prefix_chars='@')
    parser.add_argument('names', metavar='email_or_url', nargs='+',
        help="email or URL to look up; use @filename to load from a file")
    parser.add_argument('-v', '--verbose', action='store_true',
        help="show both provider name and mail server names")
    parser.add_argument('-i', '--ignore-errors', action='store_true',
        help="ignore DNS lookup errors and continue with next item")
    args = parser.parse_args(args)

    pool = Pool(processes=10)
    it = pool.imap(multiprocess_mxsniff, args.names, 10)
    try:
        for result in it:
            if args.verbose:
                print(json.dumps(result)) + ','
            else:
                print("{item}: {provider}".format(item=result['query'], provider=', '.join(result['match'])))
    except KeyboardInterrupt:
        pool.terminate()


def main():
    import os.path
    return main_internal(sys.argv[1:], os.path.basename(sys.argv[0]))

if __name__ == '__main__':
    sys.exit(main())
