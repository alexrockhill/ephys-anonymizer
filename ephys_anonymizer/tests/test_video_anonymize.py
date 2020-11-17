# -*- coding: utf-8 -*-
"""Test the video anonymization.

For each supported file format, implement a test.
"""
# Authors: Alex Rockhill <aprockhill@mailbox.org>
#
# License: BSD (3-clause)

import os.path as op
import cv2
from mne.utils import _TempDir

import ephys_anonymizer

basepath = op.join(op.dirname(ephys_anonymizer.__file__), 'tests', 'data')

face_data = dict(x=list(), y=list())
with open(op.join(basepath, 'face_data.tsv'), 'r') as fid:
    _ = fid.readline()
    for line in fid:
        x, y = line.rstrip().split('\t')
        face_data['x'].append(int(float(x)))
        face_data['y'].append(int(float(y)))


seed = (face_data['x'][0], face_data['y'][0])


def test_video_anonymize():
    out_dir = _TempDir()
    for fname in ('test_vid.mp4', 'test_vid.mov', 'test_vid.avi'):
        ext = op.splitext(fname)[-1]
        out_fname = ephys_anonymizer.video_anonymize(
            op.join(out_dir, fname), seed=seed, tmin=0, overwrite=True)
        cap = cv2.VideoCapture(out_fname)
        i = 0
        ret, frame = cap.read()
        while ret:
            ret, frame = cap.read()
            # > 7 because mov, mp4 are imprecise
            if any(frame[face_data['y'][i], face_data['x'][i]] > 7):
                raise ValueError('Face not anonymized for {}, frame {}, '
                                 'value {}'.format(ext, i,
                                                   frame[face_data['y'][i],
                                                         face_data['x'][i]]))
            ret, frame = cap.read()
            i += 1
        cap.release()
    cv2.destroyAllWindows()
