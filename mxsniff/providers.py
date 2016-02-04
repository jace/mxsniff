# -*- coding: utf-8 -*-

"""
Known email providers and their MX domains.
"""

__all__ = ['providers']

# NOTE: Please add new providers and MX servers in alphabetic order
providers = {
    'dreamhost': {'mx': [
        'mx1.sub4.homie.mail.dreamhost.com',
        'mx2.sub4.homie.mail.dreamhost.com',
    ]},
    'godaddy-us': {'mx': [
        'mailstore1.secureserver.net',
        'smtp.secureserver.net',
    ]},
    'godaddy-eu': {'mx': [
        'mailstore1.europe.secureserver.net',
        'smtp.europe.secureserver.net',
    ]},
    'godaddy-as': {'mx': [
        'mailstore1.asia.secureserver.net',
        'smtp.asia.secureserver.net',
    ]},
    'google-gmail': {'mx': [
        'alt1.gmail-smtp-in.l.google.com',
        'alt2.gmail-smtp-in.l.google.com',
        'alt3.gmail-smtp-in.l.google.com',
        'alt4.gmail-smtp-in.l.google.com',
        'gmail-smtp-in.l.google.com',
    ]},
    'google-apps': {'mx': [
        'aspmx.l.google.com',
        'alt1.aspmx.l.google.com',
        'alt2.aspmx.l.google.com',
        'alt3.aspmx.l.google.com',
        'alt4.aspmx.l.google.com',
    ]},
    'outlook-hotmail': {'mx': [
        'mx1.hotmail.com',
        'mx2.hotmail.com',
        'mx3.hotmail.com',
        'mx4.hotmail.com',
    ]},
    'pobox': {'mx': [
        'pb-mx1.pobox.com',
        'pb-mx2.pobox.com',
        'pb-mx3.pobox.com',
        'pb-mx4.pobox.com',
        'pb-mx5.pobox.com',
        'pb-mx8.pobox.com',
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
