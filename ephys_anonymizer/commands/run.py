"""Command Line Interface for video anonymization."""
# Authors: Alex Rockhill <aprockhill@mailbox.org>
#
# License: BSD (3-clause)
import argparse

import ephys_anonymizer


def video_anonymize():
    """Run video_anonymize command."""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str,
                        help='Name of the video file to anonymize. '
                        'If there are any errors be sure to enter '
                        'the full path as the first troubleshooting option')
    parser.add_argument('out_fname', nargs='?', default=None, type=str,
                        help='Filename to save out to')
    parser.add_argument('--scale', default=10, type=int, required=False,
                        help='How many neighboring pixels to use, '
                             'try scaling up or down if faces are not '
                             'being found')
    parser.add_argument('--show', default=False, type=bool, required=False,
                        help='Whether to show the anonymized video')
    parser.add_argument('--verbose', default=True, type=bool,
                        required=False,
                        help='Set verbose output to True or False.')
    parser.add_argument('--overwrite', default=False, type=bool,
                        required=False, help='Whether to overwrite')
    args = parser.parse_args()
    ephys_anonymizer.video_anonymize(args.filename, out_fname=args.out_fname,
                                     scale=args.scale, show=args.show,
                                     verbose=args.verbose,
                                     overwrite=args.overwrite)


def raw_anonymize():
    """Run raw_anonymize command."""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str,
                        help='Name of the raw file to anonymize')
    parser.add_argument('out_fname', nargs='?', default=None, type=str,
                        help='Filename to save out to')
    parser.add_argument('--verbose', default=True, type=bool,
                        required=False,
                        help='Set verbose output to True or False.')
    parser.add_argument('--overwrite', default=False, type=bool,
                        required=False, help='Whether to overwrite')
    args = parser.parse_args()
    ephys_anonymizer.raw_anonymize(args.filename, out_fname=args.out_fname,
                                   verbose=args.verbose,
                                   overwrite=args.overwrite)
