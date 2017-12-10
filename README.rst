MX Sniff
========

|travis| |coveralls|

MX Sniff identifies well known email service providers given
an email address or a domain name. Use this to find out how many
users in your email database are Gmail users (via Google Apps).

To install, get it from PyPI::

    $ pip install mxsniff

Or get the development branch direct from GitHub::

    $ pip install https://github.com/jace/mxsniff/archive/master.zip

Command line usage::

    $ mxsniff example.com gmail.com example@gmail.com https://www.google.com
    $ mxsniff -v example.com
    $ mxsniff @filename_with_list_of_domains_or_emails_or_urls
    $ mxsniff example@gmail.com -p your_email@example.com

Python usage::

    >>> from mxsniff import mxsniff, mxbulksniff
    >>> mxsniff('google.com')
    >>> mxbulksniff(['example.com', 'google.com'])  # Returns a generator with one result at a time


.. |travis| image:: https://secure.travis-ci.org/jace/mxsniff.svg
    :target: https://travis-ci.org/jace/mxsniff
    :alt: Build status

.. |coveralls| image:: https://coveralls.io/repos/github/jace/mxsniff/badge.svg?branch=master
    :target: https://coveralls.io/github/jace/mxsniff?branch=master
    :alt: Coverage status
