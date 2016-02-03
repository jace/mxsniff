# -*- coding: utf-8 -*-

"""
Known email providers and their MX domains.
"""

__all__ = ['providers']


providers = {
    'google-gmail': {'mx': [
        'gmail-smtp-in.l.google.com',
        'alt4.gmail-smtp-in.l.google.com',
        'alt1.gmail-smtp-in.l.google.com',
        'alt2.gmail-smtp-in.l.google.com',
        'alt3.gmail-smtp-in.l.google.com',
    ]},
    'google-apps': {'mx': [
        'aspmx.l.google.com',
        'alt1.aspmx.l.google.com',
        'alt2.aspmx.l.google.com',
        'alt3.aspmx.l.google.com',
        'alt4.aspmx.l.google.com',
    ]},
    'pobox': {'mx': [
        'pb-mx2.pobox.com',
        'pb-mx5.pobox.com',
        'pb-mx4.pobox.com',
        'pb-mx1.pobox.com',
        'pb-mx8.pobox.com',
        'pb-mx3.pobox.com',
    ]},
    'yahoo-mail': {'mx': [
        'mta5.am0.yahoodns.net',
        'mta6.am0.yahoodns.net',
        'mta7.am0.yahoodns.net',
        'mx-apac.mail.gm0.yahoodns.net',
        'mx-eu.mail.am0.yahoodns.net',
    ]},
    'yahoo-bizmail': {'mx': [
        'mx-biz.mail.am0.yahoodns.net',
    ]},
}
