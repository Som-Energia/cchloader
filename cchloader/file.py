from __future__ import absolute_import
from datetime import datetime
import bz2
from StringIO import StringIO
import os

from cchloader.parsers.parser import get_parser
from cchloader import logger
from cchloader.compress import get_compressed_file, is_compressed_data

class PackedCchFile(object):
    """Packed CCH file.

    Process of content of zip file is processed with iterators to keep the
    minimal memory footprint.

    Example::

        with PackedCchFile('/tmp/cch.zip') as packed:
            for cchfile in packed:
                for line in cchfile:
                    print line

    """
    def __init__(self, path, strict=False):
        """
        :param path: Packed CCH file path
        """
        self.path = path
        self.parser = get_parser(self.path)(strict=strict)
        
        self.filename = path
        self.file = get_compressed_file(path)
    
    def __iter__(self):
        return self

    def next(self):
        for filename in self.file.files:
            cch_fd = self.file.get(filename)
            sf = CchFile(filename, fd=cch_fd, parser=self.parser)
            return sf
        raise StopIteration()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the file descriptor.
        """
        self.file.close()


class CchFile(object):
    """CCH file.

    Process of content of file is processed with iterators to keep the
    minimal memory footprint.

    Example::

        with CCHFile('/tmp/cch.txt') as cch_file:
            for line in cch_file:
                print line

    :param path: Path of CCH file
    :param fd: File descriptor (use this if you have already opened the file)
    :param parser: Force to use a parser
    :param strict: Strict schema validation
    """
    def __init__(self, path, fd=None, parser=None, strict=False):
        self.path = path
        self.resume_line_number = 0
        if parser is None:
            self.parser = get_parser(self.path)(strict=strict)
        else:
            self.parser = parser
        if fd is None:
            self.fd = open(path, 'r')
        else:
            try:
                file_content = fd.read()
                # ZipExtFile has no seek method
                tmp_fd = StringIO(file_content)
                if is_compressed_data(tmp_fd):
                    # bz compressed files ina zip file
                    data = bz2.decompress(file_content)
                    bzfd = StringIO(data)
                    self.fd = bzfd
                else:
                    self.fd = tmp_fd
            except Exception as e:
                self.fd = fd

    def __iter__(self):
        return self

    def next(self):
        for line in self.fd:
            try:
                data, errors = self.parser.parse_line(line)
#                if errors:
#                    self.stats.errors.append(
#                        (self.stats.line_number, errors)
#                    )
                return data
            except Exception as exc:
                logger.critical(
                    # "Error in %s L:%s: %s %s", self.path, self.stats.line_number,
                    "Error in %s %s %s", self.path, str(exc), line, exc_info=True
                )
                if self.parser.adapter.strict:
                    raise
        raise StopIteration()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.fd.close()
