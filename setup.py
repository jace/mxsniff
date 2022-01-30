import os
import re
import sys

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
if sys.version_info.major == 2:
    README = unicode(README, 'utf-8')  # NOQA: F821
    CHANGES = unicode(CHANGES, 'utf-8')  # NOQA: F821
versionfile = open(os.path.join(here, 'mxsniff', '_version.py')).read()

mo = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", versionfile, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in mxsniff/_version.py")


setup(
    name='mxsniff',
    version=version,
    description='MX Sniffer',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Topic :: Communications :: Email',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
    author='Kiran Jonnalagadda',
    author_email='jace@pobox.com',
    url='https://github.com/jace/mxsniff',
    keywords=['mxsniff', 'email', 'mx'],
    packages=['mxsniff'],
    include_package_data=True,
    zip_safe=True,
    test_suite='tests',
    install_requires=['six', 'tldextract', 'dnspython', 'pyIsEmail'],
    entry_points={'console_scripts': ['mxsniff = mxsniff:main']},
)
