#!/usr/bin/env python
from __future__ import print_function, absolute_import

DESCRIP = 'Evalaute, write html for `.ipynb` notebook file'
EPILOG = \
"""
Opens given NBFILE as notebook.  Evaluates, writing output notebook to OUTDIR.
Writes HTML to OUTDIR.
"""
from os.path import join as pjoin, splitext, isdir, split as psplit

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
    parser.add_argument('nbfile', type=str,
                        help='notebook file')
    parser.add_argument('outdir', type=str,
                        help='directory to output files')
    parser.add_argument('--template', type=str,
                        default=DEFAULT_TEMPLATE,
                        help='html template name')
    args = parser.parse_args()
    if not isdir(args.outdir):
        raise RuntimeError('{} is not a directory'.format(args.outdir))
    write_ipynb(args.nbfile, args.outdir, template_name=args.template)


def write_ipynb(nb_path, out_dir, template_name=DEFAULT_TEMPLATE):
    fpath, fname = psplit(nb_path)
    froot, ext = splitext(fname)
    with io.open(nb_path, 'r') as f:
        nb = nbformat.read(f, DEFAULT_READ_FORMAT)
    nb.metadata['name'] = froot
    nb_evaluated = evaluate_notebook(nb, working_dir=fpath)
    with io.open(pjoin(out_dir, fname), 'wt') as f:
        nbformat.write(nb, f, DEFAULT_WRITE_FORMAT)
    nb_html = nb_to_html(nbformat.convert(nb_evaluated, HTML_FORMAT),
                         template_name=template_name,
                         resources=dict(nb_fname=fname))
    with io.open(pjoin(out_dir, froot + '.html'), 'wt') as f:
        f.write(nb_html)


if __name__ == '__main__':
    main()
