# -*- coding: utf-8 -*-

"""
Known email providers and their MX domains.
"""

__all__ = ['providers', 'public_domains']


# NOTE: Please add new providers and MX servers in alphabetic order.
# The labels `self`, `unknown` and `nomx` are reserved. Don't add them here.
# Provider names are identifiers and should never change, even if the holding
# entity has changed. Update the title instead.
# Keys:
#   mx: List of MX servers. The * wildcard is supported
#   domains: Well known email domains for this provider (optional)
#   title: Title of this provider (optional)
#   note: Explanatory note for this provider (optional)
#   url: Public URL for this provider's services (optional)
#   public: Indicates a provider of public email domains (optional, default False)
providers = {
    'i-3.com': {'mx': [
        '*.*.bak-mx.*.smtproutes.com',
        '*.*.*.bak-mx.*.smtproutes.com',
        '*.*.pri-mx.*.smtproutes.com',
        '*.*.*.pri-mx.*.smtproutes.com',
        ]},
    '1and1': {'mx': [
        '*.1and1.com',
        '*.1and1.co.uk',
        '*.1and1.fr',
        ]},
    'adista': {'mx': [
        '*.adista.fr',
        ]},
    'amazon-aws': {'mx': [
        'inbound-smtp.*.amazonaws.com',
        ],
        'title': "Amazon AWS SES",
        },
    'amazon-aws-ec2': {'mx': [
        '*.*.compute.amazonaws.com',
        ],
        'title': "Amazon AWS EC2",
        },
    'anaxa': {'mx': [
        '*.anaxanet.com',
        ]},
    'apple-icloud': {'mx': [
        '*.mail.icloud.com',
        ],
        'title': "Apple iCloud",
        'domains': ['icloud.com', 'mac.com', 'me.com'],
        'public': True,
        'canonical_flags': {'lowercase': True},
        },
    'appriver': {'mx': [
        '*.*.*.arsmtp.com',
        '*.*.*.*.arsmtp.com',
        ]},
    'aol': {'mx': [
        '*.mx.aol.com',
        ],
        'title': "AOL",
        },
    'carrierzone': {'mx': [
        '*.carrierzone.com',
        ]},
    'cologlobal': {'mx': [
        '*.cologlobal.com',
        ]},
    'cyren': {'mx': [
        '*.*.ctmail.com',
        '*.expurgate.net',
        ]},
    'cyso': {'mx': [
        '*.cyso.net',
        ]},
    'daemonmail': {'mx': [
        '*.daemonmail.com',
        ]},
    'dewile.net': {'mx': [
        'exchange.dewile.net',
        ]},
    'dreamhost': {'mx': [
        '*.mail.dreamhost.com',
        '*.*.mail.dreamhost.com',
        '*.*.*.mail.dreamhost.com',
        ],
        'title': "Dreamhost",
        },
    'easydns': {'mx': [
        'mx.easymail.ca',
        ]},
    'eapps': {'mx': [
        '*.eapps.com',
        ]},
    'emailsrvr': {'mx': [
        '*.emailsrvr.com',
        ]},
    'enom': {'mx': [
        '*.registrar-servers.com',
        ]},
    'everyone.net': {'mx': [
        '*.everyone.net',
        ]},
    'exclusivehosting': {'mx': [
        '*.exclusivehosting.net',
        ]},
    'fakemailgenerator': {'mx': [
        '*.fakemailgenerator.com',
        ],
        'public': True,
        },
    'fastmail': {'mx': [
        '*.messagingengine.com',
        ],
        'public': True,
        },
    'fatcow': {'mx': [
        'mail.fatcow.com',
        ]},
    'fireeye': {'mx': [
        '*.email.fireeyecloud.com',
        '*.*.email.fireeyecloud.com',
        ]},
    'forcepoint': {'mx': [
        '*.*.mailcontrol.com',
        ]},
    'gandi': {'mx': [
        'mail.gandi.net',
        ],
        'title': "Gandi.net",
        },
    'gmx.com': {'mx': [
        '*.gmx.com',
        '*.gmx.net',
        ],
        'title': "GMX 1&1 Mail and Media",
        'domains': ['gmx.com', 'gmx.us'],
        'public': True,
        },
    'godaddy': {'mx': [
        'mailstore1.secureserver.net',
        'smtp.secureserver.net',
        'mailstore1.europe.secureserver.net',
        'smtp.europe.secureserver.net',
        'mailstore1.asia.secureserver.net',
        'smtp.asia.secureserver.net',
        ],
        'title': "GoDaddy",
        },
    'google-gmail': {'mx': [
        'gmail-smtp-in.l.google.com',
        '*.gmail-smtp-in.l.google.com',
        ],
        'title': "Gmail",
        'url': 'https://gmail.com/',
        'domains': ['gmail.com', 'googlemail.com'],
        'public': True,
        'canonical_flags': {
            'lowercase': True,
            'strip_periods': True,
            'substitute_domains': {
                'googlemail.com': 'gmail.com'
                }
            },
        },
    'google-apps': {'mx': [
        'aspmx.l.google.com',
        '*.aspmx.l.google.com',
        '*.googlemail.com',
        'gmr-smtp-in.l.google.com',
        '*.gmr-smtp-in.l.google.com',
        '*.*.*.psmtp.com',
        '*.*.*.*.psmtp.com',
        ],
        'title': "G Suite",
        'canonical_flags': {'lowercase': True, 'strip_periods': True},
        },
    'hostcentral': {'mx': [
        '*.hostcentral.net',
        ]},
    'hostedemail': {'mx': [
        'mx.*.*.*.hostedemail.com',
        'mx.*.*.*.*.hostedemail.com',
        ]},
    'hostignition': {'mx': [
        '*.ignitionserver.net',
        ]},
    'hostinger': {'mx': [
        '*.hostinger.in',
        ]},
    'hostmonster': {'mx': [
        '*.hostmonster.com',
        ]},
    'ifastnet': {'mx': [
        'mx.byethost3.com',
        ]},
    'inbox.com': {'mx': [
        '*.inbox.com',
        ],
        'public': True,
        },
    'intermedia': {'mx': [
        '*.intermedia.net',
        ]},
    'ix': {'mx': [
        '*.ixwebhosting.com',
        ]},
    'justhost': {'mx': [
        '*.justhost.com',
        ]},
    'lfchosting': {'mx': [
        '*.loosefoot.com',
        ]},
    'liquidnet': {'mx': [
        '*.supremebox.com',
        ]},
    'logix': {'mx': [
        '*.logix.in',
        ]},
    'mail.com': {'mx': [
        '*.mail.com',
        ],
        'title': "Mail.com, a 1&1 company",
        'public': True,
        },
    'mailchimp-mandrill': {'mx': [
        '*.*.mandrillapp.com',
        ],
        'title': "Mailchimp Mandrill",
        },
    'mailhostbox': {'mx': [
        '*.mailhostbox.com',
        ]},
    'mailinator': {'mx': [
        '*.mailinator.com',
        'mx.powered.name',
        ],
        'title': "Mailinator",
        'public': True,
        },
    'mailgun': {'mx': [
        '*.mailgun.org',
        ]},
    'mcafee-mxlogic': {'mx': [
        '*.*.*.mxlogic.net',
        '*.*.*.*.mxlogic.net',
        ]},
    'megamailservers': {'mx': [
        '*.megamailservers.com',
        ]},
    'migadu': {'mx': [
        '*.migadu.com',
        ]},
    'mimecast': {'mx': [
        '*.mimecast.com',
        ]},
    'mochahost': {'mx': [
        '*.mochahost.com',
        ]},
    'mxroute': {'mx': [
        '*.mxroute.com',
        ]},
    'name.com': {'mx': [
        '*.name.com',
        ]},
    'namecheap-privateemail': {'mx': [
        '*.privateemail.com',
        ]},
    'namecheap-webhosting': {'mx': [
        '*.web-hosting.com',
        ]},
    'net4india': {'mx': [
        'mail.net4india.com',
        ]},
    'netcore': {'mx': [
        '*.netcore.co.in',
        ],
        'title': "Netcore",
        },
    'netmagic': {'mx': [
        '*.netmagicians.com',
        ]},
    'networksolutions': {'mx': [
        '*.netsolmail.net',
        '*.*.netsolmail.net',
        '*.*.*.netsolmail.net',
        '*.*.*.*.netsolmail.net',
        ],
        'title': "Network Solutions",
        },
    'one.com': {'mx': [
        '*.one.com',
        ]},
    'outlook-bizmail': {'mx': [
        '*.mail.*.outlook.com',
        ],
        'title': "Microsoft Outlook",
        },
    'outlook-hotmail': {'mx': [
        '*.hotmail.com',
        ],
        'title': "Microsoft Outlook Hotmail",
        'domains': ['hotmail.com', 'msn.com', 'outlook.co', 'outlook.com', 'live.com', 'live.in'],
        'public': True,
        'canonical_flags': {'lowercase': True},
        },
    'ovh': {'mx': [
        '*.ovh.net',
        ]},
    'pair': {'mx': [
        '*.pair.com',
        ]},
    'parklogic': {'mx': [
        '*.parklogic.com',
        ]},
    'pobox': {'mx': [
        '*.pobox.com',
        ]},
    'postmarkapp': {'mx': [
        'inbound.postmarkapp.com',
        ]},
    'poponline': {'mx': [
        '*.pop.co',
        ]},
    'private-h-email': {'mx': [
        'mail.h-email.net',
        ]},
    'private-mxproc': {'mx': [
        'mail.mxproc.com',
        ]},
    'private-nickstel': {'mx': [
        'mail.nickstel.com',
        ]},
    'private-posthost': {'mx': [
        '*.post-host.net',
        ]},
    'private-serverdata': {'mx': [
        '*.smtp.*.serverdata.net',
        ]},
    'private-usermail': {'mx': [
        '*.user-mail.net',
        ]},
    'prodigy': {'mx': [
        '*.prodigy.net',
        ]},
    'proofpoint': {'mx': [
        '*.pphosted.com',
        '*.*.pphosted.com',
        ]},
    'protonmail': {'mx': [
        '*.protonmail.ch',
        ],
        'title': "Protonmail",
        'domains': ['protonmail.com', 'protonmail.ch'],
        'public': True,
        },
    'qq': {'mx': [
        '*.qq.com',
        ]},
    'rediffmail': {'mx': [
        'mx.rediffmail.rediff.akadns.net',
        ],
        'title': "Rediffmail",
        'public': True,
        },
    'rediffmail-pro': {'mx': [
        'mail.rediffmailpro.com',
        ],
        'title': "Rediffmail Pro",
        },
    'register.com': {'mx': [
        '*.register.com',
        ]},
    'reliance-data-center': {'mx': [
        '*.rilinfo.net',
        ]},
    'runbox': {'mx': [
        'mx.runbox.com',
        ]},
    'safentrix': {'mx': [
        '*.*.safentrix.com',
        ]},
    'salushosting': {'mx': [
        'mail.salushosting.com',
        ]},
    'sendgrid': {'mx': [
        'mx.sendgrid.net'
        ],
        'title': "Sendgrid",
        },
    'servage': {'mx': [
        '*.servage.net',
        ]},
    'servergrid': {'mx': [
        '*.securedc.com',
        ]},
    'sherweb': {'mx': [
        '*.sherweb2010.com',
        ]},
    'siteground': {'mx': [
        'mailspamprotection.com',
        ]},
    'spamexperts': {'mx': [
        'mx.spamexperts.com',
        'fallbackmx.spamexperts.eu',
        'lastmx.spamexperts.net',
        ]},
    'spamh': {'mx': [
        '*.*.spamh.com',
        ]},
    'symantec-messagelabs': {'mx': [
        '*.*.messagelabs.com',
        '*.inboundmx.com',
        ]},
    'tempmail': {'mx': [
        '*.temp-mail.org',
        '*.temp-mail.ru',
        ]},
    'webcreationuk': {'mx': [
        '*.webcreationuk.com',
        ]},
    'webfaction': {'mx': [
        '*.webfaction.com',
        ]},
    'webindia': {'mx': [
        '*.webindia.com',
        ]},
    'yahoo-corp': {'mx': [
        '*.corp.*.yahoo.com',
        ]},
    'yahoo-mail': {'mx': [
        '*.am0.yahoodns.net',
        '*.mail.*.yahoodns.net',
        '*.mail.yahoo.co.jp'
        ],
        'title': "Yahoo Mail",
        'domains': ['rocketmail.com', 'yahoo.com', 'yahoo.co.uk', 'yahoo.co.in', 'ymail.com'],
        'public': True,
        'canonical_flags': {
            'lowercase': True,
            'substitute_domains': {
                'rocketmail.com': 'yahoo.com',
                'yahoo.co.uk': 'yahoo.com',
                'yahoo.co.in': 'yahoo.com',
                'ymail.com': 'yahoo.com',
                },
            },
        },
    'yandex': {'mx': [
        'mx.yandex.net',
        'mx.yandex.ru',
        ],
        'title': "Yandex",
        'domains': ['yandex.com', 'yandex.ru'],
        'public': True,
        'canonical_flags': {'lowercase': True},
        },
    'yodns': {'mx': [
        '*.yodns.com',
        ]},
    'zimbra-cloudzimail': {'mx': [
        '*.cloudzimail.com',
        ]},
    'zoho': {'mx': [
        '*.zoho.com',
        '*.zohomail.com',
        ],
        'title': "Zoho",
        'note': "Zoho provides both a public webmail service and custom domain hosting with the same MX servers",
        'canonical_flags': {'lowercase': True},
        },
    }


# This is a non-exhaustive list of popular public email domains.
# It complements the 'public' email provider flag and whitelists
# domains when the same provider also has non-public hosting, notably
# 'zoho' with zoho.com.
public_domains = {
    'gmail.com',
    'googlemail.com',
    'hotmail.com',
    'icloud.com',
    'live.com',
    'live.in',
    'mac.com',
    'mailinator.com',
    'me.com',
    'msn.com',
    'outlook.co',
    'outlook.com',
    'protonmail.ch',
    'protonmail.com',
    'rocketmail.com',
    'yahoo.co.in',
    'yahoo.co.uk',
    'yahoo.com',
    'yahoo.com',
    'yandex.com',
    'yandex.ru',
    'ymail.com',
    'zoho.com',
    }
