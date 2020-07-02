# -*- coding: utf-8 -*-
"""Anonymize a video.

Anonymize a video with a black box over any faces.
"""
# Authors: Alex Rockhill <aprockhill@mailbox.org>
#
# License: BSD (3-clause)

import sys
import os.path as op


# based on https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials
# /py_objdetect/py_face_detection/py_face_detection.html
def _find_face_and_cover(frame_gray, frame_color, cascades, scale, verbose):
    """Find faces and cover with black."""
    # get the locations of the faces
    faces = cascades[0].detectMultiScale(frame_gray, 1.1, scale)
    if len(faces) == 0:
        if verbose:
            print('No faces found trying second cascades')
        faces = cascades[1].detectMultiScale(frame_gray, 1.1, scale)
        if len(faces) == 0:
            faces = cascades[2].detectMultiScale(frame_gray, 1.1, scale)
    elif len(faces) > 1 and verbose:
        sys.stdout.write('{} faces found in frame'.format(len(faces)))
    for (x, y, w, h) in faces:
        # select the areas where the face was found
        frame_color[y: y + h, x:x + w] = 0
    return frame_color


def video_anonymize(fname, out_fname=None, scale=10, show=False,
                    verbose=True, overwrite=False):
    """Anonymize a video.

    This function will use the Viola-Jones algorithm to detect faces
    in a video and put a black box where the face is. The video is
    saved as the file name with anon added in the same directory.

    Parameters
    ----------
    fname : str
        The full file path of the video file. Currently,
        '.mov', '.mp4' and '.avi' are tested.
    out_fname : str
        The file name to save the anonymized video out to.
        Defaults to fname with '-anon.avi' after.
    scale : int
        Number of close neighbors to require. Increase if too many
        false positive faces in videos.
    show : bool
        Whether to show the new anonymized video.
        Defaults to False.
    verbose : bool
        Set verbose output to True or False.
    overwrite : bool
        Whether to overwrite the existing file.
        Defaults to False.

    Returns
    -------
    out_fname : str
        The name of the anonymized video file.
    """
    import cv2
    basename, ext = op.splitext(fname)
    if out_fname is None:
        out_fname = '{}-anon.avi'.format(basename)
    else:
        out_basename, out_ext = op.splitext(out_fname)
        out_fname = out_basename + '.avi'
    if op.isfile(out_fname) and not overwrite:
        raise ValueError('Anonymized file exists, use '
                         '`overwrite=True` to overwrite')
    if verbose:
        print('Reading in {}'.format(fname))
    cascades = [cv2.CascadeClassifier('{}{}.xml'.format(
                cv2.data.haarcascades, name)) for name in
                ('haarcascade_frontalface_default',
                 'haarcascade_profileface',
                 'haarcascade_frontalface_alt_tree',
                 'haarcascade_frontalface_alt',
                 'haarcascade_frontalface_alt2')]
    cap = cv2.VideoCapture(fname)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if ext == '.mov':
        frame_width = int(cap.get(4))
        frame_height = int(cap.get(3))
    else:
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

    out = cv2.VideoWriter(out_fname, cv2.VideoWriter_fourcc(*'MJPG'),
                          fps, (frame_width, frame_height))
    ret, frame = cap.read()
    if verbose:
        sys.stdout.write('Anonymizing .')
        sys.stdout.flush()
    while ret:
        if ext == '.mov':
            frame = frame.swapaxes(0, 1)
            frame = frame[:, ::-1]
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = _find_face_and_cover(frame_gray, frame, cascades, scale,
                                     verbose)
        out.write(frame)
        if show:
            cv2.imshow('frame', frame)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        ret, frame = cap.read()
        if verbose:
            sys.stdout.write('.')
            sys.stdout.flush()
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    if verbose:
        print('\nVideo saved to {}'.format(out_fname))
    return out_fname


def raw_anonymize(fname, out_fname=None, verbose=True, overwrite=False):
    """Anonymize a raw file.

    This function uses the mne-python anonymize functions to
    anonymize raw data or a MATLAB script from Burke Rosen 2019-05-14
    at USCD to anonymize edf files only (not recommended).

    Parameters
    ----------
    fname : str
        The full file path of the raw file. Currently,
        '.fif'
    out_fname : str
        The file name to save the anonymized raw file out to.
        Defaults to fname with '-anon-raw.fif' after.
    verbose : bool
        Set verbose output to True or False.
    overwrite : bool
        Whether to overwrite the existing file.
        Defaults to False.

    Returns
    -------
    out_fname : str
        The name of the anonymized video file.
    """
    import mne
    basename, ext = op.splitext(fname)
    if out_fname is None:
        out_fname = '{}-anon-raw.fif'.format(basename)
    else:
        out_basename, out_ext = op.splitext(out_fname)
        if out_basename[-4:] in ('-raw', '_raw'):
            out_fname = out_basename + '.fif'
        else:
            out_fname = out_basename + '-raw.fif'
    if op.isfile(out_fname) and not overwrite:
        raise ValueError('Anonymized file exists, use '
                         '`overwrite=True` to overwrite')
    if verbose:
        print('Reading in {}'.format(fname))
    if ext == '.fif':
        raw = mne.io.read_raw_fif(fname, preload=False)
    elif ext == '.edf':
        raw = mne.io.read_raw_edf(fname, preload=False)
    elif ext == 'bdf':
        raw = mne.io.read_raw_bdf(fname, preload=False)
    elif ext == '.vhdr':
        raw = mne.io.read_raw_brainvision(fname, preload=False)
    elif ext == '.set':
        raw = mne.io.read_raw_eeglab(fname, preload=False)
    else:
        raise ValueError('Extension {} not recognized, options are'
                         'fif, edf, bdf, vhdr (brainvision) and set '
                         '(eeglab)'.format(ext))
    if verbose:
        print('Anonymizing')
    raw.anonymize()
    if verbose:
        print('Saving to {}'.format(out_fname))
    raw.save(out_fname, overwrite=overwrite)
    return out_fname
