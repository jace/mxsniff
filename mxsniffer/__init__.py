# -*- coding: utf-8 -*-

"""
MX Sniffer identifies common email service providers given an email address or a domain name.
"""

from __future__ import absolute_import
from six import text_type
from six.moves.urllib.parse import urlparse
from email.utils import parseaddr
import dns.resolver
import tldextract

from ._version import __version__, __version_info__  # NOQA
from .providers import providers

__all__ = ['MXLookupException', 'get_domain', 'mxsniff', 'mxbulksniff']


provider_domains = {}

for name, domains in providers.items():
    for domain in domains:
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


def mxsniff(email_or_domain, ignore_errors=False):
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
    """
    domain = get_domain(email_or_domain)

    result = []

    try:
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

    if len(result) == 0:
        return None
    elif len(result) == 1:
        return result[0]
    else:
        return result


def mxbulksniff(items, ignore_errors=True):
    """
    Identify the email service provider of a large set of domains or emails, caching to avoid
    repeat queries.

    >>> sorted(mxbulksniff(['example.com', 'google.com', 'http://www.google.com']).items())
    [('example.com', None), ('google.com', 'google-apps'), ('http://www.google.com', 'google-apps')]
    """
    domain_cache = {}
    results = {}
    for i in items:
        domain = get_domain(i)
        results[i] = domain_cache[domain] if domain in domain_cache else mxsniff(domain, ignore_errors)
    return results
