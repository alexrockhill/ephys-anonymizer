"""
==================================
01. Anonymize Video and Ephys Data
==================================

In this example, we anonymize both a video and a fif file with eeg data.

.. currentmodule:: ephys_anonymizer

.. _BrainVision format: https://www.brainproducts.com/productdetails.php?id=21&tab=5
.. _CapTrak: http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined/#details-of-the-captrak-coordinate-system

"""  # noqa: E501

# Authors: Alex Rockhill <aprockhill@mailbox.org>
#
# License: BSD (3-clause)

###############################################################################
# We are importing everything we need for this example:
import os

import mne
import ephys_anonymizer

from ephys_anonymizer import video_anonymize, raw_anonymize

###############################################################################
# Anonymize
# ---------
#
# Anonymize a raw file and a video file

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_raw.fif')
raw_anonymize(sample_data_raw_file, overwrite=True)

sample_video_fname = os.path.join(os.path.dirname(ephys_anonymizer.__file__),
                                  'tests', 'data', 'test_vid.avi')
video_anonymize(sample_video_fname, overwrite=True)
