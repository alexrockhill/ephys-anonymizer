# -*- coding: utf-8 -*-
"""Test the raw anonymization.

For each supported file format, implement a test.
"""
# Authors: Alex Rockhill <aprockhill@mailbox.org>
#
# License: BSD (3-clause)

import os.path as op
import mne
from mne.datasets import testing

import pytest
from numpy.testing import assert_array_almost_equal
from mne.utils import _TempDir

import ephys_anonymizer

basepath = op.join(op.dirname(ephys_anonymizer.__file__), 'tests', 'data')

data_path = testing.data_path()
fif_fname = op.join(data_path, 'MEG', 'sample',
                    'sample_audvis_trunc_raw.fif')
edf_fname = op.join(data_path, 'EDF', 'test_reduced.edf')

raw_fif = mne.io.read_raw_fif(fif_fname)
raw_edf = mne.io.read_raw_edf(edf_fname)


@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_raw_anonymize():
    out_dir = _TempDir()
    out_fname = op.join(out_dir, 'test-anon-raw.fif')
    ephys_anonymizer.raw_anonymize(fif_fname, out_fname=out_fname)
    raw = mne.io.read_raw_fif(out_fname)
    assert raw.info['meas_date'].year == 2000
    assert raw.info['meas_date'].month == 1
    assert raw.info['meas_date'].day == 1
    assert raw.info['experimenter'] == 'mne_anonymize'
    assert_array_almost_equal(raw.get_data(), raw.get_data(), decimal=10)

    ephys_anonymizer.raw_anonymize(edf_fname, out_fname, overwrite=True)
    raw = mne.io.read_raw_fif(out_fname)
    assert_array_almost_equal(raw.get_data(), raw.get_data(), decimal=10)
