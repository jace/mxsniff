"""
MX Sniff identifies common email service providers from an address or domain.
"""

from collections import namedtuple
from email.utils import parseaddr
from functools import partial
from urllib.parse import urlparse
import smtplib
import socket
import sys

from pyisemail import is_email
from tldextract import TLDExtract
import dns.resolver

from ._version import __version__, __version_info__  # NOQA: F401
from .providers import providers as all_providers
from .providers import public_domains

__all__ = ['MxLookupError', 'MXLookupException', 'get_domain', 'mxsniff', 'mxbulksniff']

_value = object()  # Used in WildcardDomainDict as a placeholder
tldextract = TLDExtract(suffix_list_urls=None)  # Don't fetch TLDs during a sniff
ResultCodeMessage = namedtuple('ResultCodeMessage', ['result', 'code', 'message'])


class MxLookupError(Exception):
    """Exception raised when MX records cannot be looked up."""


# XXX: Legacy name
MXLookupException = MxLookupError


class WildcardDomainDict:
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
    >>> d['example.wildcard.com']
    Traceback (most recent call last):
        ...
    KeyError: 'example.wildcard.com'
    """

    def __init__(self, *args, **kwargs):
        self.tree = dict(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__ + '(' + repr(self.tree) + ')'

    @staticmethod
    def _makeparts(key):
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
            else:
                raise KeyError(key)
        if _value in tree:
            return tree[_value]
        raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


provider_mx = WildcardDomainDict()
provider_domains = {}


def __populate_dicts(pmx, pd):
    for name, data in all_providers.items():
        for domain in data['mx']:
            pmx[domain] = name
        if 'domains' in data:
            for domain in data['domains']:
                pd[domain] = name


__populate_dicts(provider_mx, provider_domains)


def canonical_email(
    email, lowercase=False, strip_periods=False, substitute_domains=None
):
    """
    Return a canonical representation of an email address to facilitate string
    comparison::

        >>> canonical_email('Example <example+extra@example.com>')
        'example@example.com'
        >>> canonical_email('Exam.ple@gmail.com', lowercase=True, strip_periods=True)
        'example@gmail.com'
    """
    if substitute_domains is None:
        substitute_domains = {}
    # Example <example+extra@Example.com> --> example+extra@Example.com
    addr = parseaddr(email)[1]
    if not is_email(addr):
        return
    # example+extra@Example.com --> example+extra, Example.com
    mailbox, domain = addr.split('@', 1)
    # example+extra --> example
    if '+' in mailbox:
        mailbox = mailbox[: mailbox.find('+')]
    if strip_periods and '.' in mailbox:
        mailbox = mailbox.replace('.', '')
    if lowercase:
        mailbox = mailbox.lower()
    # Example.com --> example.com
    domain = domain.lower()
    # googlemail.com --> gmail.com
    if domain in substitute_domains:
        domain = substitute_domains[domain]
    # example, example.com --> example@example.com
    return '%s@%s' % (mailbox, domain)


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
        addr = parseaddr(email_or_domain)[1]
        domain = addr.split('@', 1)[-1]
    elif '//' in email_or_domain:
        domain = tldextract(
            urlparse(email_or_domain).netloc.split(':')[0]
        ).registered_domain
    else:
        domain = email_or_domain.strip()
    return domain.lower()


def provider_info(provider):
    """
    Return a copy of the provider dict with only public fields
    """
    if provider in all_providers:
        return {
            'name': provider,
            'title': all_providers[provider].get('title'),
            'note': all_providers[provider].get('note'),
            'url': all_providers[provider].get('url'),
            'public': all_providers[provider].get('public', False),
        }


def mxsniff(
    email_or_domain,
    ignore_errors=False,
    cache=None,
    timeout=30,
    use_static_domains=True,
):
    """
    Lookup MX records and identify the email service provider(s).

    Accepts an email address, URL or domain name, and looks up an internal list of
    well known providers.

    :param str email_or_domain: Email, domain or URL to lookup
    :param bool ignore_errors: Fail silently if there's a DNS lookup error
    :param dict cache: Cache with a dictionary interface to avoid redundant lookups
    :param int timeout: Timeout in seconds
    :param bool use_static_domains: Speed up lookups by using the static domain list in
        the provider database
    :return: Matching domain, MX servers, and identified service provider(s)
    :raises MxLookupError: If a DNS lookup error happens and ``ignore_errors`` is
        False

    >>> mxsniff('example.com')['match']
    ['nullmx']
    >>> mxsniff('__invalid_domain_name__.com')['match']
    ['nomx']
    >>> mxsniff('example@gmail.com')['match']
    ['google-gmail']
    >>> sorted(mxsniff('https://google.com/').keys())
    ['canonical', 'domain', 'match', 'mx', 'providers', 'public', 'query']
    """
    domain = get_domain(email_or_domain)
    if cache is not None and domain in cache:
        result = dict(cache[domain])
        result['query'] = email_or_domain
        return result

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
            mx_answers = sorted(
                (rdata.preference, rdata.exchange.to_text(omit_final_dot=True).lower())
                for rdata in resolver.query(domain, 'MX')
            )
            for _preference, exchange in mx_answers:
                # Extract the top-level domain for testing for self-hosted email later
                rdomain = tldextract(exchange).registered_domain
                if rdomain not in tld:
                    tld.append(rdomain)
                # Check if the provider is known from the MX record
                provider = provider_mx.get(exchange)
                if provider and provider not in matches:
                    matches.append(provider)
                    rproviders.append(provider_info(provider))
        except (
            dns.resolver.NoAnswer,
            dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers,
        ):
            pass
        except dns.exception.DNSException as e:
            if ignore_errors:
                pass
            else:
                raise MxLookupError(e, domain)

    if not matches:
        # Check for self-hosted email servers; identify them with the label 'self'
        if tldextract(domain).registered_domain in tld:
            matches.append('self')
        if not matches:
            if mx_answers:
                if mx_answers[0][1] == '.':
                    matches.append('nullmx')  # Email not accepted (RFC 7505)
                else:
                    matches.append('unknown')  # We don't know this one's provider
            else:
                matches.append('nomx')  # This domain has no mail servers

    if matches:
        canonical = canonical_email(
            email_or_domain,
            **all_providers.get(matches[0], {}).get('canonical_flags', {}),
        )
    else:
        canonical = canonical_email(email_or_domain)

    result = {
        'query': email_or_domain,
        'domain': domain,
        'match': matches,
        'mx': mx_answers,
        'providers': rproviders,
        'public': domain in public_domains or any(p['public'] for p in rproviders),
        'canonical': canonical,
    }
    if cache is not None:
        cache[domain] = result
    return result


def mxprobe(email, mx, your_email, hostname=None, timeout=30):
    """
    Probe an email address at an MX server

    :param str email: Email address to be probed
    :param mx: MX server(s) to do the test at; will be tried in order until one is
        available
    :param your_email: Your email address, to perform the probe
    :param hostname: Optional hostname to perform the probe with
    :return: :attr:`ResultCodeMessage`, a 3-tuple of result, SMTP code and explanatory
        message

    Possible results:

    * invalid: This is not an email address
    * error: The MX servers could not be probed
    * fail: The email address doesn't appear to exist, but further investigation is
        necessary
    * soft-fail: The email address is currently not accepting email
    * hard-fail: The email address does not exist
    * pass: The email address appears to exist
    * pass-unverified: Mail server is accepting email but can't verify existence

    >>> mxprobe('jackerhack@gmail.com', 'gmail-smtp-in.l.google.com', 'example@example.com')[0]
    'pass'
    >>> mxprobe('foo@gmail.com', 'gmail-smtp-in.l.google.com', 'example@example.com')[0]
    'hard-fail'
    >>> mxprobe('example@example.com', [], 'example@example.com', timeout=5)[0]
    'error'
    >>> mxprobe('example.com', [], 'example@example.com').result
    'invalid'
    """
    if not hostname:
        hostname = 'probe.' + your_email.split('@', 1)[-1].strip()
    email = parseaddr(email)[1]
    if not is_email(email):
        return ResultCodeMessage('invalid', None, None)
    if not mx:
        mx = [email.split('@', 1)[-1].strip()]
    if isinstance(mx, str):
        mx = [mx]
    error_code = None
    error_msg = None
    for mxserver in mx:
        probe_result = None
        try:
            smtp = smtplib.SMTP(mxserver, 25, hostname, timeout)
            smtp.ehlo_or_helo_if_needed()
            code, msg = smtp.mail(your_email)
            msg = str(msg, 'utf-8')
            if code != 250:
                error_code = code
                error_msg = msg
                continue
            # Supply the email address as a recipient and see how the server responds
            code, msg = smtp.rcpt(email)
            msg = str(msg, 'utf-8')
            # List of codes from
            # http://support.mailhostbox.com/email-administrators-guide-error-codes/
            # 250 – Requested mail action completed and OK
            if code == 250:
                probe_result = ResultCodeMessage('pass', code, msg)
            # 251 – Not Local User, forward email to forward path
            # 252 – Cannot Verify user, will attempt delivery later
            # 253 – Pending messages for node started
            elif code in (251, 252, 253):
                probe_result = ResultCodeMessage('pass-unverified', code, msg)
            elif code in (
                450,  # Requested mail action not taken: mailbox unavailable. Request
                #       refused
                451,  # Requested action aborted: local error in processing. Request is
                #       unable to be processed, try again
                452,  # Requested action not taken: insufficient system storage
                510,  # Check the recipient address
                512,  # Domain can not be found. Unknown host.
                515,  # Destination mailbox address invalid
                521,  # Domain does not accept mail
                522,  # Recipient has exceeded mailbox limit
                531,  # Mail system Full
                533,  # Remote server has insufficient disk space to hold email
                540,  # Email address has no DNS Server
                550,  # Requested action not taken: mailbox unavailable
                551,  # User not local; please try forward path
                552,  # Requested mail action aborted: exceeded storage allocation
                553,  # Requested action not taken: mailbox name not allowed
            ):
                # Some servers return ESMTP codes prefixed with #, others don't
                if msg.startswith(('4.', '#4.')):
                    r = 'soft-fail'
                elif msg.startswith(('5.', '#5.')):
                    r = 'hard-fail'
                else:
                    r = 'fail'
                probe_result = ResultCodeMessage(r, code, msg)
            else:  # Unknown code
                error_code = code
                error_msg = msg
        except smtplib.SMTPResponseException as e:
            error_code = e.smtp_code
            error_msg = e.smtp_error
        except (smtplib.SMTPException, socket.error) as e:
            error_code = None
            error_msg = str(e)
            continue
        # Probe complete. Quit the connection, ignoring errors
        try:
            smtp.rset()
            smtp.quit()
        except smtplib.SMTPException:  # pragma: no cover
            pass
        # Did we get a result? Return it
        if probe_result is not None:
            return probe_result
        # If no result, continue to the next MX server

    # We couldn't talk to any MX server
    return ResultCodeMessage('error', error_code, error_msg)


def mxbulksniff(items, ignore_errors=True):
    """
    Identify the email service provider of a large set of domains or emails, caching to
    avoid repeat queries. Returns a generator that yields one item at a time

    >>> [(i['query'], i['match']) for i in mxbulksniff(
    ...     ['example.com', 'google.com', 'http://www.google.com', 'example.com'])]
    [('example.com', ['nullmx']), ('google.com', ['google-apps']), ('http://www.google.com', ['google-apps']), ('example.com', ['nullmx'])]
    """
    cache = {}
    for i in items:
        yield mxsniff(i, ignore_errors, cache)


def mxsniff_and_probe(email, probe_email, timeout=30, **kwargs):
    """
    Combine :func:`mxsniff` and :func:`mxprobe` into a single result
    """
    result = mxsniff(email, timeout=timeout, **kwargs)
    if probe_email:
        result['probe'] = mxprobe(
            email, [mx[1] for mx in result['mx']], probe_email, timeout=timeout
        )
    return result


def main_internal(args, name='mxsniff'):
    """
    Console script

    >>> main_internal(['example@gmail.com'])  # doctest: +ELLIPSIS
    example@gmail.com,google-gmail...
    >>> main_internal(['example@gmail.com', '-p', 'example@gmail.com'])  # doctest: +ELLIPSIS
    example@gmail.com,hard-fail,...
    >>> main_internal(['example.com', '-v'])
    [
    {"canonical": null, "domain": "example.com", "match": ["nullmx"], "mx": [[0, "."]], "providers": [], "public": false, "query": "example.com"}
    ]
    >>> main_internal(['Example <exam.ple+extra@googlemail.com>', '-v'])  # doctest: +ELLIPSIS
    [
    {"canonical": "example@gmail.com", "domain": "googlemail.com", "match": ["google-gmail"], "mx": [...], "providers": [...], "public": true, "query": "Example <exam.ple+extra@googlemail.com>"}
    ]
    """
    from multiprocessing.dummy import Pool
    import argparse
    import csv
    import json

    parser = argparse.ArgumentParser(
        prog=name,
        description="Identify email service providers given an email address, URL or"
        " domain name",
        fromfile_prefix_chars='@',
    )
    parser.add_argument(
        'names',
        metavar='email_or_url',
        nargs='+',
        help="email or URL to look up; use @filename to load from a file",
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help="return verbose results in JSON"
    )
    parser.add_argument(
        '-i',
        '--ignore-errors',
        action='store_true',
        help="ignore DNS lookup errors and continue with next item",
    )
    parser.add_argument(
        '-t',
        '--timeout',
        type=int,
        metavar='T',
        default=30,
        help="DNS timeout in seconds (default: %(default)s)",
    )
    parser.add_argument(
        '-p',
        '--probe',
        metavar='your_email',
        default=None,
        help="probe whether target email address exists (needs your email to perform"
        " the test)",
    )
    args = parser.parse_args(args)

    # Assume non-Unicode names to be in UTF-8
    names = [n.decode('utf-8') if not isinstance(n, str) else n for n in args.names]

    pool = Pool(processes=10 if not args.probe else 1)
    it = pool.imap_unordered(
        partial(
            mxsniff_and_probe,
            probe_email=args.probe,
            ignore_errors=args.ignore_errors,
            timeout=args.timeout,
            use_static_domains=False,
        ),
        names,
        10,
    )
    try:
        if args.verbose:
            # Valid JSON output hack
            firstline = True
            print('[')  # NOQA: T001
            for result in it:
                if firstline:
                    firstline = False
                else:
                    print(',')  # NOQA: T001
                print(json.dumps(result, sort_keys=True), end='')  # NOQA: T001
            print('\n]')  # NOQA: T001
        else:
            out = csv.writer(sys.stdout)
            for result in it:
                if args.probe:
                    out.writerow([result['query']] + list(result['probe']))
                else:
                    out.writerow([result['query']] + result['match'])
    except KeyboardInterrupt:  # pragma: no cover
        pool.terminate()
        raise


def main():  # pragma: no cover
    import os.path

    return main_internal(sys.argv[1:], os.path.basename(sys.argv[0]))


if __name__ == '__main__':
    sys.exit(main())
