from __future__ import absolute_import

import click
from cchloader.file import CchFile, PackedCchFile
from cchloader.backends import get_backend
from cchloader.compress import is_compressed_file

@click.group()
def cchloader():
    pass


@cchloader.command(name="import")
@click.option('--file', help="CCH File to import", type=click.Path(exists=True), required=True)
@click.option('--backend', help="Backend url", required=True)
def import_file(file, backend):
    url = backend
    backend = get_backend(backend)
    lines = []
    with backend(url) as bnd:
        if is_compressed_file(file):
            click.echo("Using packed CCH File for {}".format(file))
            with PackedCchFile(file) as psf:
                for cch_file in psf:
                    print cch_file.path
                    for line in cch_file:
                        if not line:
                            continue
                        lines.append(line)
        else:
            with CchFile(file) as cch_file:
                for line in cch_file:
                    if not line:
                        continue
                    lines.append(line)
        bnd.insert_batch(lines)


if __name__ == "__main__":
    cchloader()
