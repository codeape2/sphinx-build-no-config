from argparse import ArgumentParser
import tempfile
from pathlib import Path
import shutil

from sphinx.application import Sphinx


def create_temp_directory_structure() -> Path:
    rootdir = Path(tempfile.mkdtemp())
    for subdir in ['confdir', 'srcdir']:
        (rootdir / subdir).mkdir()
    return rootdir


def write_config(confpyfile: Path):
    confpyfile.write_text('', encoding='utf8')


def main():
    parser = ArgumentParser()
    parser.add_argument('filename', type=Path)
    args = parser.parse_args()
    rootdir = create_temp_directory_structure()
    write_config(rootdir / 'confdir' / 'conf.py')
    shutil.copy(args.filename, rootdir / 'srcdir' / 'index.rst')
    try:
        app = Sphinx(
            srcdir=rootdir / 'srcdir',
            confdir=rootdir / 'confdir',
            outdir=rootdir / 'outdir',
            doctreedir=rootdir / 'doctreedir',
            buildername='singlehtml'
        )
        app.build()
    finally:
        shutil.rmtree(rootdir)


if __name__ == '__main__':
    main()