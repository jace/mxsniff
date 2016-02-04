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


provider_domains = {}

for name, data in providers.items():
    for domain in data['mx']:
        provider_domains[domain.lower()] = name


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


def mxsniff(email_or_domain, verbose=False, ignore_errors=False):
    """
    Lookup MX records for a given email address, URL or domain name and identify the email service provider(s)
    from an internal list of known service providers.

    :param str email_or_domain: Email, domain or URL to lookup
    :return: Identified service provider, or a list if there's more than one (in unusual circumstances)

    >>> mxsniff('example.com')
    >>> mxsniff('__invalid_domain_name__.com')
    >>> mxsniff('example@gmail.com')
    'google-gmail'
    >>> mxsniff('https://google.com/')
    'google-apps'
    >>> sorted(mxsniff('google.com', verbose=True).items())
    [('match', ['google-apps']), ('mx', [(10, 'aspmx.l.google.com'), (20, 'alt1.aspmx.l.google.com'), (30, 'alt2.aspmx.l.google.com'), (40, 'alt3.aspmx.l.google.com'), (50, 'alt4.aspmx.l.google.com')]), ('name', 'google.com')]
    """
    domain = get_domain(email_or_domain)

    result = []

    try:
        answers = []  # Default value in case of verbose mode where an error occurs
        answers = sorted([(rdata.preference, rdata.exchange.to_text(omit_final_dot=True).lower())
            for rdata in dns.resolver.query(domain, 'MX')])
        for preference, exchange in answers:
            if exchange in provider_domains:
                provider = provider_domains[exchange]
                if provider not in result:
                    result.append(provider)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        pass
    except dns.exception.DNSException as e:
        if ignore_errors:
            pass
        else:
            raise MXLookupException('{exc} {error} ({domain})'.format(
                exc=e.__class__.__name__, error=text_type(e), domain=domain))

    if verbose:
        return {'name': email_or_domain, 'match': result, 'mx': answers}
    else:
        if len(result) == 0:
            return None
        elif len(result) == 1:
            return result[0]
        else:
            return result


def mxbulksniff(items, verbose=False, ignore_errors=True):
    """
    Identify the email service provider of a large set of domains or emails, caching to avoid
    repeat queries. Returns a generator that yields one item at a time

    >>> list(mxbulksniff(['example.com', 'google.com', 'http://www.google.com']))
    [('example.com', None), ('google.com', 'google-apps'), ('http://www.google.com', 'google-apps')]
    """
    domain_cache = {}
    for i in items:
        domain = get_domain(i)
        yield i, domain_cache[domain] if domain in domain_cache else mxsniff(domain, verbose, ignore_errors)


def main_internal(args, name='mxsniff'):
    """
    Console script

    >>> main_internal(['example@gmail.com'])
    example@gmail.com: google-gmail
    """
    import argparse
    parser = argparse.ArgumentParser(
        prog=name,
        description='Identify email service providers given an email address, URL or domain name',
        fromfile_prefix_chars='@')
    parser.add_argument('names', metavar='email_or_url', nargs='+',
        help="email or URL to look up; use @filename to load from a file")
    parser.add_argument('-v', '--verbose', action='store_true',
        help="show both provider name and mail server names")
    parser.add_argument('-i', '--ignore-errors', action='store_true',
        help="ignore DNS lookup errors and continue with next item")
    args = parser.parse_args(args)
    for item, provider in mxbulksniff(args.names, verbose=args.verbose, ignore_errors=args.ignore_errors):
        print("{item}: {provider}".format(item=item, provider=provider))


def main():
    import os.path
    return main_internal(sys.argv[1:], os.path.basename(sys.argv[0]))

if __name__ == '__main__':
    sys.exit(main())
