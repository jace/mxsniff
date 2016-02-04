0.2.2
=====

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
