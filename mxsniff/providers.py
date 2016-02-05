# -*- coding: utf-8 -*-

"""
Known email providers and their MX domains.
"""

__all__ = ['providers']

# NOTE: Please add new providers and MX servers in alphabetic order
providers = {
    '1and1': {'mx': [
        '*.1and1.com',
        ]},
    'amazon-aws': {'mx': [
        'inbound-smtp.*.amazonaws.com',
        ]},
    'amazon-aws-ec2': {'mx': [
        '*.*.compute.amazonaws.com',
        ]},
    'apple-icloud': {'mx': [
        '*.mail.icloud.com',
        ]},
    'dreamhost': {'mx': [
        '*.mail.dreamhost.com',
        '*.*.mail.dreamhost.com',
        '*.*.*.mail.dreamhost.com',
        ]},
    'emailsrvr': {'mx': [
        '*.emailsrvr.com',
        ]},
    'fatcow': {'mx': [
        'mail.fatcow.com',
        ]},
    'gandi': {'mx': [
        'mail.gandi.net',
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
    'netmagic': {'mx': [
        '*.netmagicians.com',
        ]},
    'one.com': {'mx': [
        '*.one.com'
        ]},
    'outlook-bizmail': {'mx': [
        '*.mail.*.outlook.com',
        ]},
    'outlook-hotmail': {'mx': [
        '*.hotmail.com',
        ]},
    'pobox': {'mx': [
        '*.pobox.com',
        ]},
    'proofpoint': {'mx': [
        '*.*.pphosted.com',
        ]},
    'rediffmail': {'mx': [
        'mx.rediffmail.rediff.akadns.net',
        ]},
    'rediffmail-pro': {'mx': [
        'mail.rediffmailpro.com',
        ]},
    'servage': {'mx': [
        '*.servage.net',
        ]},
    'siteground': {'mx': [
        'mailspamprotection.com',
        ]},
    'symantec-messagelabs': {'mx': [
        '*.*.messagelabs.com',
        ]},
    'webfaction': {'mx': [
        '*.webfaction.com'
        ]},
    'yahoo-mail': {'mx': [
        'mta5.am0.yahoodns.net',
        'mta6.am0.yahoodns.net',
        'mta7.am0.yahoodns.net',
        'mx-apac.mail.gm0.yahoodns.net',
        'mx-eu.mail.am0.yahoodns.net',
        'mx1.mail.yahoo.co.jp',
        'mx2.mail.yahoo.co.jp',
        'mx3.mail.yahoo.co.jp',
        'mx5.mail.yahoo.co.jp',
        ]},
    'yahoo-bizmail': {'mx': [
        'mx-biz.mail.am0.yahoodns.net',
        'mx-indiabiz.mail.gm0.yahoodns.net',
        ]},
    'yandex': {'mx': [
        'mx.yandex.ru',
        ]},
    'zoho': {'mx': [
        '*.zoho.com',
        '*.zohomail.com',
        ]},
}
