import os
import re
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = unicode(open(os.path.join(here, 'README.rst')).read(), 'utf-8')
CHANGES = unicode(open(os.path.join(here, 'CHANGES.rst')).read(), 'utf-8')
versionfile = open(os.path.join(here, "mxsniffer", "_version.py")).read()

mo = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", versionfile, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in mxsniffer/_version.py.")


setup(name='mxsniffer',
    version=version,
    description='MX Sniffer',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries",
        ],
    author='Kiran Jonnalagadda',
    author_email='jace@pobox.com',
    url='https://github.com/jace/mxsniffer',
    keywords=['mxsniffer', 'email', 'mx'],
    packages=['mxsniffer'],
    include_package_data=True,
    zip_safe=True,
    test_suite='tests',
    install_requires=['dnspython'],
    )
