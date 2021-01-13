#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
import zipfile
import gzip
import bz2

class CompressedFile (object):
    magic = None
    file_type = None
    mime_type = None
    proper_extension = None

    def __init__(self, filename):
        self.filename = filename

    @classmethod
    def is_magic(self, data):
        return data.startswith(self.magic)

    def open(self):
        return None

    def close(self):
        self.fd.close()


class ZIPFile (CompressedFile):
    magic = '\x50\x4b\x03\x04'
    file_type = 'zip'
    mime_type = 'compressed/zip'

    def __init__(self, filename):
        super(ZIPFile, self).__init__(filename)
        self.fd = self.open()
        self.files = self.list()        

    def open(self):
        return zipfile.ZipFile(self.filename)

    def list(self):
        return iter(self.fd.namelist())

    def get(self, filename):
        return self.fd.open(filename)


class GZFile (CompressedFile):
    magic = '\x1f\x8b\x08'
    file_type = 'gz'
    mime_type = 'compressed/gz'

    def __init__(self, filename):
        super(GZFile, self).__init__(filename)
        self.fd = self.open()
        self.files = self.list()

    def open(self):
        return gzip.GzipFile(self.filename)

    def list(self):
        gf = self.fd.fileobj
        
        gf.seek(2)
        method, flag, mtime = struct.unpack("<BBIxx", gf.read(8))

        if not flag & gzip.FNAME:
            # Not stored in the header, use the filename sans .gz
            fname = self.fd.name
            if fname.endswith('.gz'):
                fname = fname[:-3]
            gf.seek(0)
            return iter([fname])

        if flag & gzip.FEXTRA:
            # Read & discard the extra field, if present
            gf.read(struct.unpack("<H", gf.read(2)))        

        # Read a null-terminated string containing the filename
        fname = []
        while True:
            s = gf.read(1)
            if not s or s == '\000':
                break
            fname.append(s)
        gf.seek(0)
        return iter([''.join(fname)])

    def get(self, filename):
        return self.fd


class BZFile (CompressedFile):
    magic = '\x42\x5a\x68'
    file_type = 'bz2'
    mime_type = 'compressed/bz'

    def __init__(self, filename):
        super(BZFile, self).__init__(filename)
        self.fd = self.open()
        self.files = self.list()

    def open(self):
        return bz2.BZ2File(self.filename)

    def list(self):
        # BZ2 file does not include original filename
        fname = self.fd.name
        if fname.endswith('.bz2'):
            fname = fname[:-3]
        return iter([fname])

    def get(self, filename):
        return self.fd


class FileTypeNotSupportedException(Exception):
    pass


def is_compressed_data(fd):
    start_of_file = fd.read(5)
    fd.seek(0)
    for cls in (ZIPFile, GZFile, BZFile):
        if cls.is_magic(start_of_file):
            return True

    return False

def is_compressed_file(filename):
    with file(filename, 'rb') as f:
        start_of_file = f.read(5)
        f.seek(0)
        for cls in (ZIPFile, GZFile, BZFile):
            if cls.is_magic(start_of_file):
                return True
        return False

def get_compressed_file(filename):
    with file(filename, 'rb') as f:
        start_of_file = f.read(5)
        f.seek(0)
        for cls in (ZIPFile, GZFile, BZFile):
            if cls.is_magic(start_of_file):
                return cls(filename)

        raise FileTypeNotSupportedException
