#!/usr/bin/env python
from __future__ import print_function, absolute_import

DESCRIP = 'Evalaute, write html for `.ipynb` notebook files'
EPILOG = \
"""
Looks for files in directory INDIR with extension '.ipynb'. Opens found files
as notebook(s).  Evaluates, writing output notebook to OUTDIR.  Writes HTML to
OUTDIR.
"""
import sys
import os
from os.path import join as pjoin, splitext, dirname


from argparse import ArgumentParser, RawDescriptionHelpFormatter

from write_ipynb import write_ipynb

DEFAULT_TEMPLATE = 'perrinate.tpl'


def main():
    parser = ArgumentParser(description=DESCRIP,
                            epilog=EPILOG,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('indir', type=str,
                        help='directory in which to search')
    parser.add_argument('outdir', type=str,
                        help='directory to output files')
    parser.add_argument('--template', type=str,
                        default=DEFAULT_TEMPLATE,
                        help='html template name')
    parser.add_argument('--verbose', action='store_true',
                        help='print more messages')
    args = parser.parse_args()
    for fname in os.listdir(args.indir):
        if fname.startswith('.'):
            continue
        froot, ext = splitext(fname)
        if not ext == '.ipynb':
            continue
        fullpath = pjoin(args.indir, fname)
        if args.verbose:
            print('Processing ' + fullpath)
        write_ipynb(fullpath, args.outdir, args.template)


if __name__ == '__main__':
    main()
