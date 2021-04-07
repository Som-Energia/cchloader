from expects import expect, equal, raise_error
from cchloader.parsers.parser import *
from cchloader.parsers.f1 import F1
from cchloader.parsers.p1 import P1
from cchloader.parsers.p2 import P2
from cchloader.parsers.epfpf import EPFPF
from cchloader.exceptions import ParserNotFoundException
from cchloader.file import PackedCchFile


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
        self.epfpf_filenames = ['EPFPF_HD_GEN_1234_P1_20200201.1.ZIP', 'EPFPF_H2_CLE_0762_P2_20201101.0.ZIP',]
        self.wrong_filename = 'P1_20170507_20170706.6'

    with it('test to get F1 parser'):
        for filename in self.f1_filenames:
            expect(get_parser(filename)).to(equal(F1))
    with it('F1 parser fits file format'):
        with PackedCchFile('spec/curve_files/F1_0031_20190507.1.ZIP') as packed:
            for cch_file in packed:
                for line in cch_file:
                    expected_f1 = 'ES0031408433164001SV0F;11;2019/05/01 00:00:00;1;1;0;0;0;0;0;0;0;5;0;\r\n'
                    result_f1 = line['orig']
                    assert result_f1 == expected_f1
                    break
                break

    with it('test to get P1 parser'):
        for filename in self.p1_filenames:
            expect(get_parser(filename)).to(equal(P1))
    with it('P1 parser fits file format'):
        with PackedCchFile('spec/curve_files/P1D_0031_0762_20190608.1.ZIP') as packed:
            for cch_file in packed:
                for line in cch_file:
                    expected_p1 = 'ES0031408381283001EW1P;11;2019/06/08 00:00:00;1;20.000;0;0.000;0;3.000;0;0.000;0;0.000;0;0.000;0;0.000;128;0.000;128;1;0\n'
                    result_p1 = line['orig']
                    assert result_p1 == expected_p1
                    break
                break

    with it('test to get P2 parser'):
        for filename in self.p2_filenames:
            expect(get_parser(filename)).to(equal(P2))
    with it('P2 parser fits file format'):
        with PackedCchFile('spec/curve_files/P2D_0031_0762_20190615.2.ZIP') as packed:
            for cch_file in packed:
                for line in cch_file:
                    expected_p2 = 'ES0031408528975003CB2P;11;2019/06/15 00:00:00;1;0;0;0;0;0;0;0;0;0;0;0;0;0;128;0;128;1\n'
                    result_p2 = line['orig']
                    assert result_p2 == expected_p2
                    break
                break

    with it('test to get EPFPF parser'):
        for filename in self.epfpf_filenames:
            expect(get_parser(filename)).to(equal(EPFPF))
    with it('EPFPF parser fits file format'):
        for filename in self.epfpf_filenames:
            with PackedCchFile('spec/curve_files/' + filename) as packed:
                for cch_file in packed:
                    for line in cch_file:
                        result_p2 = line['orig']
                        pass

    with it('test error to get exception'):
        def test_raise_error():
            get_parser(self.wrong_filename)

        expect(test_raise_error).to(raise_error(
            ParserNotFoundException))
