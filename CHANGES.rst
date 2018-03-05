0.3.3
=====

* ``mxprobe`` now distinguishes between soft and hard fails
* ``mxsniff`` command line now produces valid CSV or JSON (verbose mode)
* Verbose output now includes canonical representation of an email address to facilitate comparison

0.3.2
=====

* Fix PyPI distribution (no code changes)

0.3.1
=====

* The providers list now includes provider metadata (title, note, url)
* Public email domains are now tagged and identified in results
* A static domain list is included for very popular domains (typically public email domains)
* The command line script now handles IDN names correctly
* Email probe feature, to attempt a guess on whether the email is actually valid

0.3.0
=====

* Added support for wildcards in domain names
* Additional providers
* Detect self-hosted email servers
* Remove verbose mode in the mxsniff function; always verbose now
* Track MX TLDs
* Run queries in a multiprocess pool in the command line version

0.2.1
=====

* Updated README and minor bugfixes

0.2.0
=====

* Python 3 and PyPy support
* ``mxsniff`` now returns a string or None, switching to a list only when multiple service providers are found
* ``get_domain`` now extracts the TLD when a URL is provided, so ``www.`` and other subdomains are ignored
* New ``mxbulksniff`` to run on a large list
* Verbose mode to also retrieve MX values
* New console script for easy use and batch processing of large lists
* More providers

0.1.0
=====

* First version
