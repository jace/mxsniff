MX Sniff
========

.. image:: https://secure.travis-ci.org/jace/mxsniff.svg
    :target: https://travis-ci.org/jace/mxsniff
    :alt: Build status

.. image:: https://coveralls.io/repos/github/jace/mxsniff/badge.svg?branch=master
    :target: https://coveralls.io/github/jace/mxsniff?branch=master
    :alt: Coverage status

MX Sniff identifies well known email service providers given
an email address or a domain name. Use this to find out how many
users in your email database are Gmail users (via Google Apps).

Command line usage::

    $ mxsniff example.com gmail.com
    $ mxsniff -v example.com
    $ mxsniff @filename

Python usage::

    >>> from mxsniff import mxsniff, mxbulksniff
    >>> mxsniff('example@gmail.com')
    'google-gmail'
    >>> mxsniff('https://google.com/')
    'google-apps'
    >>> mxsniff('google.com', verbose=True)
    {'match': ['google-apps'], 'mx': [(10, 'aspmx.l.google.com'), (20, 'alt1.aspmx.l.google.com'), (30, 'alt2.aspmx.l.google.com'), (40, 'alt3.aspmx.l.google.com'), (50, 'alt4.aspmx.l.google.com')], 'name': 'google.com'}

    >>> list(mxbulksniff(['example.com', 'google.com', 'http://www.google.com']))
    [('example.com', None), ('google.com', 'google-apps'), ('http://www.google.com', 'google-apps')]
