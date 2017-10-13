# -*- coding: utf-8 -*-

"""
MX Sniffer identifies common email service providers given an email address or a domain name.
"""

from __future__ import absolute_import, print_function
import sys
from functools import partial
from six import text_type
from six.moves.urllib.parse import urlparse
from email.utils import parseaddr
import dns.resolver
import tldextract

from ._version import __version__, __version_info__  # NOQA
from .providers import providers as all_providers, public_domains

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


provider_mx = WildcardDomainDict()
provider_domains = {}

for name, data in all_providers.items():
    for domain in data['mx']:
        provider_mx[domain] = name
    if 'domains' in data:
        for domain in data['domains']:
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
    return domain.lower()


def provider_info(provider):
    """
    Return a copy of the provider dict with only public fields
    """
    if provider in all_providers:
        return {
            'title': all_providers[provider].get('title'),
            'note': all_providers[provider].get('note'),
            'url': all_providers[provider].get('url'),
            'public': all_providers[provider].get('public', False),
            }


def mxsniff(email_or_domain, ignore_errors=False, cache=None, timeout=30, use_static_domains=True):
    """
    Lookup MX records for a given email address, URL or domain name and identify the email service provider(s)
    from an internal list of known service providers.

    :param str email_or_domain: Email, domain or URL to lookup
    :param bool ignore_errors: Fail silently if there's a DNS lookup error
    :param dict cache: Cache with a dictionary interface to avoid redundant lookups
    :return: Matching domain, MX servers, and identified service provider(s)
    :raises MXLookupException: If a DNS lookup error happens and ``ignore_errors`` is False

    >>> mxsniff('example.com')['match']
    ['nomx']
    >>> mxsniff('__invalid_domain_name__.com')['match']
    ['nomx']
    >>> mxsniff('example@gmail.com')['match']
    ['google-gmail']
    >>> sorted(mxsniff('https://google.com/').keys())
    ['domain', 'match', 'mx', 'providers', 'public', 'query']
    """
    domain = get_domain(email_or_domain)
    if cache and domain in cache:
        return cache[domain]

    #: Providers that matched
    matches = []
    #: Info on matching providers (title, note, url, public)
    rproviders = []
    #: Top-level of MX domain (used to detect self-hosted email)
    tld = []
    #: Default return value for MX in case an error occurs and is ignored
    mx_answers = []

    if use_static_domains and domain in provider_domains:
        matches.append(provider_domains[domain])
        rproviders.append(provider_info(provider_domains[domain]))
    else:
        try:
            # Use a DNS resolver with custom timeout
            resolver = dns.resolver.Resolver()
            resolver.timeout = timeout
            resolver.lifetime = timeout
            # Get answers, sorted by MX preference
            mx_answers = sorted([(rdata.preference, rdata.exchange.to_text(omit_final_dot=True).lower())
                for rdata in resolver.query(domain, 'MX')])
            for preference, exchange in mx_answers:
                # Extract the top-level domain for testing for self-hosted email later
                rdomain = tldextract.extract(exchange).registered_domain
                if rdomain not in tld:
                    tld.append(rdomain)
                # Check if the provider is known from the MX record
                provider = provider_mx.get(exchange)
                if provider and provider not in matches:
                    matches.append(provider)
                    rproviders.append(provider_info(provider))
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            pass
        except dns.exception.DNSException as e:
            if ignore_errors:
                pass
            else:
                raise MXLookupException('{exc} {error} ({domain})'.format(
                    exc=e.__class__.__name__, error=text_type(e), domain=domain))

    if not matches:
        # Check for self-hosted email servers; identify them with the label 'self'
        if tldextract.extract(domain).registered_domain in tld:
            matches.append('self')
        if not matches:
            if mx_answers:
                matches.append('unknown')  # We don't know this one's provider
            else:
                matches.append('nomx')  # This domain has no mail servers

    result = {
        'query': email_or_domain,
        'domain': domain,
        'match': matches,
        'mx': mx_answers,
        'providers': rproviders,
        'public': domain in public_domains or any([p['public'] for p in rproviders])
        }
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


def main_internal(args, name='mxsniff'):
    """
    Console script

    >>> main_internal(['example@gmail.com'])
    example@gmail.com: google-gmail
    """
    import argparse
    import json
    from multiprocessing.dummy import Pool

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
    parser.add_argument('-t', '--timeout', type=int, metavar='T', default=30,
        help="DNS timeout in seconds (default: %(default)s)")
    args = parser.parse_args(args)

    # Assume non-Unicode names to be in UTF-8
    names = [n.decode('utf-8') if not isinstance(n, text_type) else n for n in args.names]

    pool = Pool(processes=10)
    it = pool.imap_unordered(
        partial(mxsniff,
            ignore_errors=args.ignore_errors,
            timeout=args.timeout,
            use_static_domains=False),
        names,
        10)
    try:
        for result in it:
            if args.verbose:
                print(json.dumps(result)) + ','
            else:
                print(u"{item}: {provider}".format(item=result['query'], provider=', '.join(result['match'])))
    except KeyboardInterrupt:
        pool.terminate()
        raise


def main():
    import os.path
    return main_internal(sys.argv[1:], os.path.basename(sys.argv[0]))

if __name__ == '__main__':
    sys.exit(main())
