# -*- coding: utf-8 -*-
"""Anonymize a video.

Anonymize a video with a black box over any faces.
"""
# Authors: Alex Rockhill <aprockhill@mailbox.org>
#
# License: BSD (3-clause)

import sys
import os.path as op
import numpy as np
import cv2

MAX_BUFFER_S = 2
TOLERANCE = 0.1


def _click_event(event, x, y, flags, param):
    """Handle the click event to seed the face finder."""
    global click_x, click_y
    if event == cv2.EVENT_LBUTTONDOWN:
        click_x, click_y = x, y


def _seed_face(frame_color):
    cv2.imshow('seed face selector', frame_color)
    cv2.setMouseCallback('seed face selector', _click_event)
    global click_x, click_y
    click_x = click_y = None
    while click_x is None or click_y is None:
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
    return click_x, click_y


# based on https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials
# /py_objdetect/py_face_detection/py_face_detection.html
def _find_face(frame_gray, cascades, seed, scale, neighbors, verbose=True):
    """Find faces and cover with black."""
    sx, sy = seed
    # get the locations of the faces
    for name, cascade in cascades.items():
        faces = cascade.detectMultiScale(frame_gray, scale, neighbors)
        for (x, y, w, h) in faces:
            if abs(x + w / 2 - sx) / sx + abs(y + h / 2 - sy) / sy < TOLERANCE:
                if 'eye' in name:
                    return x - w * 3, y - h * 3, w * 6, h * 6
                else:
                    return x, y, w, h
    return None


def video_anonymize(fname, out_fname=None, scale=1.05, neighbors=1, seed=None,
                    tmin=5, min_size=0.03, max_size=0.1, overwrite=False,
                    verbose=True):
    """Anonymize a video.

    This function will use the Viola-Jones algorithm to detect faces
    in a video and put a black box where the face is. The video is
    saved as the file name with anon added in the same directory.

    Parameters
    ----------
    fname: str
        The full file path of the video file. Currently,
        '.mov', '.mp4' and '.avi' are tested.
    out_fname: str
        The file name to save the anonymized video out to.
        Defaults to fname with '-anon.mp4' after.
    scale: float
        How finely to process the image, closer to 1 is more finely.
    neighbors: int
        Number of close neighbors to require. Increase if too many
        false positive faces in videos.
    seed: tuple
        Where to start finding the face. If None, the seed will be chosen by
        clicking.
    tmin: float
        The time in seconds to start the anonymized video.
    min_size: float
        The minimum size of the box as a proportion of width.
    max_size:
        The maximum size of the box as a proportion of width.
    overwrite: bool
        Whether to overwrite the existing file.
        Defaults to False.
    verbose: bool
        Set verbose output to True or False.

    Returns
    -------
    out_fname : str
        The name of the anonymized video file.
    """
    basename, ext = op.splitext(fname)
    if out_fname is None:
        out_fname = '{}-anon.mp4'.format(basename)
    else:
        out_basename, out_ext = op.splitext(out_fname)
        out_fname = out_basename + '.mp4'
    if op.isfile(out_fname) and not overwrite:
        raise ValueError('Anonymized file exists, use '
                         '`overwrite=True` to overwrite')
    if verbose:
        print('Reading in {}'.format(fname))
    cascades = {name: cv2.CascadeClassifier('{}{}.xml'.format(
        cv2.data.haarcascades, name)) for name in
        ('haarcascade_frontalface_default',
         'haarcascade_profileface',
         'haarcascade_eye')}
    cap = cv2.VideoCapture(fname)
    fps = cap.get(cv2.CAP_PROP_FPS)
    max_buffer_len = np.round(MAX_BUFFER_S * fps)
    if ext == '.mov':
        frame_width = int(cap.get(4))
        frame_height = int(cap.get(3))
    else:
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
    min_pixel_size = np.round(frame_width * min_size).astype(int)
    max_pixel_size = np.round(frame_width * max_size).astype(int)

    out = cv2.VideoWriter(out_fname, cv2.VideoWriter_fourcc(*'mp4v'),
                          fps, (frame_width, frame_height))
    ret, frame = cap.read()
    i = 0
    while ret and i < tmin:
        ret, frame = cap.read()
        i += 1 / fps

    if seed is None:
        if verbose:
            print('Please click on the face to be anonymized to '
                  'seed the algorithm so that it gets the right one')
        seed = _seed_face(frame)

    frame_buffer = list()
    if verbose:
        sys.stdout.write('Anonymizing .')
        sys.stdout.flush()
    while ret:
        if ext == '.mov':
            frame = frame.swapaxes(0, 1)
            frame = frame[:, ::-1]
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = _find_face(frame_gray, cascades, seed, scale,
                          neighbors, verbose=verbose)
        if face is None or min(face[2:]) < min_pixel_size or \
                max(face[2:]) > max_pixel_size:
            frame_buffer.append(frame)
            if len(frame_buffer) > max_buffer_len:
                cap.release()
                out.release()
                cv2.destroyAllWindows()
                raise ValueError(f'Video anonymization failure, there '
                                 f'were more than {max_buffer_len} frames '
                                 'without detecting a face, '
                                 'report to developers')
        else:
            x, y, w, h = face
            frame[y: y + h, x:x + w] = 0
            if len(frame_buffer) > 0:
                n_interp = len(frame_buffer)
                if verbose:
                    plural = 's' if n_interp > 1 else ''
                    sys.stdout.write(f'Interpolating {n_interp} frame{plural}')
                    sys.stdout.flush()
                fx, fy = x + w / 2, y + h / 2
                sx, sy = seed
                xs = list(np.round(
                    np.linspace(sx, fx, n_interp) - w / 2).astype(int))
                ys = list(np.round(
                    np.linspace(sy, fy, n_interp) - h / 2).astype(int))
                while frame_buffer:
                    bframe, x, y = frame_buffer.pop(0), xs.pop(0), ys.pop(0)
                    bframe[y: y + h, x:x + w] = 0
                    out.write(bframe)
                seed = fx, fy
            out.write(frame)
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
    anonymize raw data.

    Parameters
    ----------
    fname : str
        The full file path of the raw file.
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
    elif ext == '.bdf':
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
