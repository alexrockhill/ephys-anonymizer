"""Command Line Interface for MNE-BIDS."""
# Authors: Teon Brooks <teon.brooks@gmail.com>
#          Stefan Appelhoff <stefan.appelhoff@mailbox.org>
#
# License: BSD (3-clause)
import argparse

import video_anonymize


def main():
    """Run main command."""
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
    parser.add_argument('--n_cascades', default=1, type=int, required=False,
                        help='Number of cascades to use, try scaling up '
                             'if faces are not being found')
    parser.add_argument('--show', default=False, type=bool, required=False,
                        help='Whether to show the anonymized video')
    parser.add_argument('--verbose', default=True, type=bool,
                        required=False,
                        help='Set verbose output to True or False.')
    parser.add_argument('--overwrite', default=False, type=bool,
                        required=False, help='Whether to overwrite')
    args = parser.parse_args()
    video_anonymize.video_anonymize(args.filename, out_fname=args.out_fname,
                                    scale=args.scale,
                                    n_cascades=args.n_cascades,
                                    show=args.show, verbose=args.verbose,
                                    overwrite=args.overwrite)
