#! /usr/bin/env python
"""Setup ephys_anonymizer."""
import os
from setuptools import setup, find_packages

# get the version
version = None
with open(os.path.join('ephys_anonymizer', '__init__.py'), 'r') as fid:
    for line in (line.strip() for line in fid):
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('\'')
            break
if version is None:
    raise RuntimeError('Could not determine version')


descr = ('ephys_anonymizer: Use the Viola-Jones algorithm to anonymize '
         'faces with a black box and anonymize electrophysiology '
         'data with mne-python')

DISTNAME = 'ephys_anonymizer'
DESCRIPTION = descr
MAINTAINER = 'Alex Rockhill'
MAINTAINER_EMAIL = 'aprockhill@mailbox.org'
URL = 'https://github.com/alexrockhill/ephys_anonymizer/'
LICENSE = 'BSD (3-clause)'
DOWNLOAD_URL = 'https://github.com/alexrockhill/ephys_anonymizer.git'
VERSION = version

if __name__ == "__main__":
    setup(name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          long_description=open('README.rst').read(),
          long_description_content_type='text/x-rst',
          python_requires='~=3.5',
          classifiers=[
              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',
              'License :: OSI Approved',
              'Programming Language :: Python',
              'Topic :: Software Development',
              'Topic :: Scientific/Engineering',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX',
              'Operating System :: Unix',
              'Operating System :: MacOS',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
              'Programming Language :: Python :: 3.7',
          ],
          platforms='any',
          packages=find_packages(),
          entry_points={'console_scripts': [
              'video_anonymize = '
              'ephys_anonymizer.commands.run:video_anonymize',
              'raw_anonymize = '
              'ephys_anonymizer.commands.run:raw_anonymize'
          ]},
          project_urls={
              'Bug Reports':
                  'https://github.com/alexrockhill/ephys_anonymizer/issues',
              'Source': 'https://github.com/alexrockhill/ephys_anonymizer',
          },
          install_requires=[
              'opencv-python',
              'mne'
          ]
          )
