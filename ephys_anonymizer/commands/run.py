"""Command Line Interface for video anonymization."""
# Authors: Alex Rockhill <aprockhill@mailbox.org>
#
# License: BSD (3-clause)
import argparse

import ephys_anonymizer


def video_anonymize():
    """Run video_anonymize command.

    example usage:  $ video_anonymize fname out_fname --scale 1.3
                      --neighbors 5 --tmin 3 --verbose True --overwrite True
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str,
                        help='Name of the video file to anonymize. '
                        'If there are any errors be sure to enter '
                        'the full path as the first troubleshooting option')
    parser.add_argument('out_fname', default=None, type=str, nargs='?',
                        help='Filename to save out to')
    parser.add_argument('--scale', default=1.05, type=float, required=False,
                        help='How fine of a resolution to use to parse '
                             'the image')
    parser.add_argument('--neighbors', default=1, type=int, required=False,
                        help='How many neighboring pixels to use, '
                             'try scaling up or down if faces are not '
                             'being found')
    parser.add_argument('--seed', default=None, nargs=2, type=int,
                        help='Where the first face is in pixels, if not '
                             'provided, a frame will be shown to click')
    parser.add_argument('--tmin', default=5, type=float, required=False,
                        help='The time in seconds to start the anonymized '
                             'video')
    parser.add_argument('--min_size', default=0.03, type=float, required=False,
                        help='The minimum size of the box as a'
                             'proportion of width.')
    parser.add_argument('--max_size', default=0.1, type=float, required=False,
                        help='The maximum size of the box as a'
                             'proportion of width.')
    parser.add_argument('--verbose', default=True, type=bool,
                        required=False,
                        help='Set verbose output to True or False.')
    parser.add_argument('-o', '--overwrite', action='store_true',
                        help='Pass this flag to overwrite an existing file')
    args = parser.parse_args()
    if args.out_fname is not None and len(args.out_fname) > 1:
        raise ValueError('Only one out_fname can be used as a positional '
                         f'argument, got {args.out_fname}')
    ephys_anonymizer.video_anonymize(
        args.filename, out_fname=args.out_fname, scale=args.scale,
        neighbors=args.neighbors, seed=args.seed, tmin=args.tmin,
        min_size=args.min_size, max_size=args.max_size,
        overwrite=args.overwrite, verbose=args.verbose)


def raw_anonymize():
    """Run raw_anonymize command.

    example usage:  $ raw_anonymize fname out_fname
                      --verbose True --overwrite True
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str,
                        help='Name of the raw file to anonymize')
    parser.add_argument('out_fname', nargs='?', default=None, type=str,
                        help='Filename to save out to')
    parser.add_argument('--verbose', default=True, type=bool,
                        required=False,
                        help='Set verbose output to True or False.')
    parser.add_argument('-o', '--overwrite', action='store_true',
                        help='Pass this flag to overwrite an existing file')
    args = parser.parse_args()
    if args.out_fname is not None and len(args.out_fname) > 1:
        raise ValueError('Only one out_fname can be used as a positional '
                         f'argument, got {args.out_fname}')
    ephys_anonymizer.raw_anonymize(args.filename, out_fname=args.out_fname,
                                   overwrite=args.overwrite,
                                   verbose=args.verbose)
