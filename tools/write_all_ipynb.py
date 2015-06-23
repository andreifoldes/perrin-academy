#!/usr/bin/env python
from __future__ import print_function, absolute_import

DESCRIP = 'Evalaute, write html for `.ipynb` notebook files'
EPILOG = \
"""
Looks for files in directory INDIR with extension '.ipynb'. Opens found files
as notebook(s).  Evaluates, writing output notebook to OUTDIR.  Writes HTML to
OUTDIR.
"""
import os
from os.path import join as pjoin, splitext, isdir
from copy import deepcopy

import io

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import IPython.nbformat as nbformat
from IPython.nbconvert import html
from runipy.notebook_runner import NotebookRunner

DEFAULT_TEMPLATE = 'perrinate.tpl'
DEFAULT_READ_FORMAT = 3
DEFAULT_WRITE_FORMAT = 3
HTML_FORMAT = 4


def evaluate_notebook(nb, working_dir=None):
    # Create evaluated version and save it to the dest path.
    nb_runner = NotebookRunner(nb=nb, working_dir=working_dir)
    nb_runner.run_notebook()
    return nb_runner.nb


def nb_to_html(nb, template_name=DEFAULT_TEMPLATE, resources=None):
    """convert notebook to html
    """
    exporter = html.HTMLExporter(template_file=template_name)
    full_resources = dict(metadata = nb.metadata)
    if resources is not None:
        full_resources.update(resources)
    output, resources = exporter.from_notebook_node(nb,
                                                    resources=full_resources)
    return output


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
    if not isdir(args.outdir):
        raise RuntimeError('{} is not a directory'.format(args.outdir))
    for fname in os.listdir(args.indir):
        if fname.startswith('.'):
            continue
        froot, ext = splitext(fname)
        if not ext == '.ipynb':
            continue
        fullpath = pjoin(args.indir, fname)
        if args.verbose:
            print('Processing ' + fullpath)
        with io.open(fullpath, 'r') as f:
            nb = nbformat.read(f, DEFAULT_READ_FORMAT)
        nb.metadata['name'] = froot
        nb_evaluated = evaluate_notebook(nb, working_dir=args.indir)
        with io.open(pjoin(args.outdir, fname), 'wt') as f:
            nbformat.write(nb, f, DEFAULT_WRITE_FORMAT)
        nb_html = nb_to_html(nbformat.convert(nb_evaluated, HTML_FORMAT),
                             resources=dict(nb_fname=fname))
        with io.open(pjoin(args.outdir, froot + '.html'), 'wt') as f:
            f.write(nb_html)


if __name__ == '__main__':
    main()
