# -*- coding: utf-8 -*-
"""Anonymize a video.

Anonymize a video with a black box over any faces.
"""
# Authors: Alex Rockhill <aprockhill@mailbox.org>
#
# License: BSD (3-clause)

import os.path as op
import argparse
import cv2

cascades = [cv2.CascadeClassifier('{}{}.xml'.format(
            cv2.data.haarcascades, name)) for name in
            ('haarcascade_frontalface_default',
             'haarcascade_profileface',
             'haarcascade_frontalface_alt_tree',
             'haarcascade_frontalface_alt.xml',
             'haarcascade_frontalface_alt2.xml')]


# based on https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials
# /py_objdetect/py_face_detection/py_face_detection.html
def _find_face_and_cover(frame_gray, frame_color, scale, n_cascades):
    """Find faces and cover with black"""
    # check all cascades to be sure
    for cascade in cascades[:n_cascades]:
        # get the locations of the faces
        faces = cascade.detectMultiScale(frame_gray, 1.1, scale)
        for (x, y, w, h) in faces:
            # select the areas where the face was found
            frame_color[y: y + h, x:x + w] = 0
    return frame_color


def video_anonymize(fname, n_cascades=1, scale=10, show=False,
                    overwrite=False):
    """Anonymize a video

    This function will use the Viola-Jones algorithm to detect faces
    in a video and put a black box where the face is. The video is
    saved as the file name with anon added in the same directory.

    Parameters
    ----------
    fname : str
        The full file path of the video file. Currently,
        '.mov', '.mp4' and '.avi' are tested.
    n_cascades : int
        Number of cascades to use. More cascades, less false negatives
        but also probably more false positives and it takes longer.
    show : bool
        Whether to show the new anonymized video.
        Defaults to False.
    overwrite : bool
        Whether to overwrite the existing file.
        Defaults to False.

    Returns
    -------
    out_fname : str
        The name of the anonymized video file.
    """
    if n_cascades > 5:
        raise ValueError('There are only five cascades that I can find')
    basename, ext = op.splitext(fname)
    out_fname = '{}-anon.avi'.format(basename)
    if op.isfile(out_fname) and not overwrite:
        raise ValueError('Anonymized file exists, use '
                         '`overwrite=True` to overwrite')
    cap = cv2.VideoCapture(fname)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    out = cv2.VideoWriter(out_fname, cv2.VideoWriter_fourcc(*'MJPG'),
                          fps, (frame_width, frame_height))
    ret, frame = cap.read()
    while ret:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = _find_face_and_cover(frame_gray, frame, scale, n_cascades)
        out.write(frame)
        if show:
            cv2.imshow('frame', frame)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        ret, frame = cap.read()
    cap.release()
    out.release()
    return out_fname


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, required=True,
                        help='Name of the video file to anonymize. '
                        'If there are any errors be sure to enter '
                        'the full path as the first troubleshooting option')
    parser.add_argument('--scale', default=10, type=int, required=False,
                        help='How many neighboring pixels to use, '
                             'try scaling up or down if faces are not '
                             'being found')
    parser.add_argument('--n_cascades', default=1, type=int, required=False,
                        help='Number of cascades to use, try scaling up '
                             'if faces are not being found')
    parser.add_argument('--show', type=bool, required=False,
                        help='Whether to show the anonymized video')
    parser.add_argument('--overwrite', type=bool, required=False,
                        help='Whether to overwrite')
    args = parser.parse_args()
    video_anonymize(args.filename, args.show, args.overwrite)
    cv2.destroyAllWindows()
