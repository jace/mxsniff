# -*- coding: utf-8 -*-

"""
Known email providers and their MX domains.
"""

__all__ = ['providers']

# NOTE: Please add new providers and MX servers in alphabetic order
providers = {
    'amazon-aws': {'mx': [
        'inbound-smtp.*.amazonaws.com',
    ]},
    'dreamhost': {'mx': [
        '*.mail.dreamhost.com',
        '*.*.mail.dreamhost.com',
        '*.*.*.mail.dreamhost.com',
    ]},
    'emailsrvr': {'mx': [
        'emailsrvr.com',
    ]},
    'fatcow': {'mx': [
        'mail.fatcow.com',
    ]},
    'godaddy': {'mx': [
        'mailstore1.secureserver.net',
        'smtp.secureserver.net',
        'mailstore1.europe.secureserver.net',
        'smtp.europe.secureserver.net',
        'mailstore1.asia.secureserver.net',
        'smtp.asia.secureserver.net',
    ]},
    'google-gmail': {'mx': [
        'gmail-smtp-in.l.google.com',
        '*.gmail-smtp-in.l.google.com',
    ]},
    'google-apps': {'mx': [
        'aspmx.l.google.com',
        '*.aspmx.l.google.com',
    ]},
    'mailhostbox': {'mx': [
        '*.mailhostbox.com',
    ]},
    'one.com': {'mx': [
        '*.one.com'
    ]},
    'outlook-bizmail': {'mx': [
        '*.mail.protection.outlook.com',
    ]},
    'outlook-hotmail': {'mx': [
        '*.hotmail.com',
    ]},
    'pobox': {'mx': [
        '*.pobox.com',
    ]},
    'siteground': {'mx': [
        'mailspamprotection.com',
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
        'mx-indiabiz.mail.gm0.yahoodns.net',
    ]},
    'zoho': {'mx': [
        '*.zoho.com',
        '*.zohomail.com',
    ]},
}
