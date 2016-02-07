# -*- coding: utf-8 -*-

"""
Known email providers and their MX domains.
"""

__all__ = ['providers']

# NOTE: Please add new providers and MX servers in alphabetic order.
# The labels `self`, `unknown` and `nomx` are reserved. Don't add them here
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
        ]},
    'amazon-aws-ec2': {'mx': [
        '*.*.compute.amazonaws.com',
        ]},
    'anaxa': {'mx': [
        '*.anaxanet.com',
        ]},
    'apple-icloud': {'mx': [
        '*.mail.icloud.com',
        ]},
    'appriver': {'mx': [
        '*.*.*.arsmtp.com',
        '*.*.*.*.arsmtp.com',
        ]},
    'aol': {'mx': [
        '*.mx.aol.com',
        ]},
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
        ]},
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
    'exclusivehosting': {'mx': [
        '*.exclusivehosting.net',
        ]},
    'fakemailgenerator': {'mx': [
        '*.fakemailgenerator.com',
        ]},
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
        ]},
    'gmx.com': {'mx': [
        '*.gmx.com',
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
        '*.googlemail.com',
        'gmr-smtp-in.l.google.com',
        '*.gmr-smtp-in.l.google.com',
        '*.*.*.psmtp.com',
        '*.*.*.*.psmtp.com',
        ]},
    'h-email': {'mx': [
        'mail.h-email.net',
        ]},
    'hostcentral': {'mx': [
        '*.hostcentral.net',
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
    'mailchimp-mandrill': {'mx': [
        '*.*.mandrillapp.com',
        ]},
    'mailhostbox': {'mx': [
        '*.mailhostbox.com',
        ]},
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
    'mimecast': {'mx': [
        '*.mimecast.com',
        ]},
    'mochahost': {'mx': [
        '*.mochahost.com',
        ]},
    'mxproc': {'mx': [
        'mail.mxproc.com',
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
        ]},
    'netmagic': {'mx': [
        '*.netmagicians.com',
        ]},
    'networksolutions': {'mx': [
        '*.netsolmail.net',
        '*.*.netsolmail.net',
        '*.*.*.netsolmail.net',
        '*.*.*.*.netsolmail.net',
        ]},
    'one.com': {'mx': [
        '*.one.com',
        ]},
    'outlook-bizmail': {'mx': [
        '*.mail.*.outlook.com',
        ]},
    'outlook-hotmail': {'mx': [
        '*.hotmail.com',
        ]},
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
    'qq': {'mx': [
        '*.qq.com',
        ]},
    'rediffmail': {'mx': [
        'mx.rediffmail.rediff.akadns.net',
        ]},
    'rediffmail-pro': {'mx': [
        'mail.rediffmailpro.com',
        ]},
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
        ]},
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
        ]},
    'yandex': {'mx': [
        'mx.yandex.net',
        'mx.yandex.ru',
        ]},
    'yodns': {'mx': [
        '*.yodns.com',
        ]},
    'zimbra-cloudzimail': {'mx': [
        '*.cloudzimail.com',
        ]},
    'zoho': {'mx': [
        '*.zoho.com',
        '*.zohomail.com',
        ]},
}
