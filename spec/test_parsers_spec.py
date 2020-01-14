from expects import expect, equal, raise_error
from cchloader.parsers.parser import *
from cchloader.parsers.f1 import F1
from cchloader.parsers.p1 import P1
from cchloader.parsers.p2 import P2
from cchloader.exceptions import ParserNotFoundException


with description('Testing of parsers'):

    with before.all:

        self.f1_filenames = [
            'F1_0022_20170507_20170706.6',  # Documented
            'F1_0022_0706_20170507_20170706.6', # Fenosa
            'F1_0031_20170216.1.ZIP', # Endesa
        ]
        self.p1_filenames = [
            'P1_0022_20170507_20170706.6',  # Documented
            'P1_0022_0706_20170507_20170706.6',  # Fenosa
            'P1_0031_20170311.1.ZIP',  # Endesa
        ]
        self.p2_filenames = [
            'P2_0022_20170507_20170706.6',  # Documented
            'P2_0022_0706_20170507_20170706.6',  # Fenosa
            'P2_0031_20170311.1.ZIP',  # Endesa
        ]
        self.wrong_filename = 'P1_20170507_20170706.6'

    with it('test to get F1 parser'):
        for filename in self.f1_filenames:
            expect(get_parser(filename)).to(equal(F1))

    with it('test to get P1 parser'):
        for filename in self.p1_filenames:
            expect(get_parser(filename)).to(equal(P1))

    with it('test to get P2 parser'):
        for filename in self.p2_filenames:
            expect(get_parser(filename)).to(equal(P2))

    with it('test error to get exception'):
        def test_raise_error():
            get_parser(self.wrong_filename)

        expect(test_raise_error).to(raise_error(
            ParserNotFoundException))
