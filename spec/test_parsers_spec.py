# -*- coding: utf-8 -*-
from mamba import description, before, it
from expects import expect, equal, raise_error
from cchloader.parsers.parser import *
from cchloader.parsers.f1 import F1
from cchloader.parsers.p1 import P1
from cchloader.parsers.p2 import P2
from cchloader.parsers.epfpf import EPFPF

from cchloader.parsers.a5d import A5d
from cchloader.parsers.b5d import B5d
from cchloader.parsers.rf5d import Rf5d
from cchloader.parsers.mhcil import Mhcil
from cchloader.parsers.medidas import Medidas
from cchloader.parsers.corbagen import CorbaGen
from cchloader.parsers.infpa import Infpa
from cchloader.exceptions import ParserNotFoundException
from cchloader.file import PackedCchFile, CchFile


with description('Testing of parsers'):

    with before.all:

        self.epfpf_filenames = [
            'EPFPF_HD_GEN_1234_P1_20200201.1.bz2'
        ]
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
        self.a5d_filenames = [
            'A5D_4321_1234_20170507.0',  # Documented
            'A5D_0189_0373_20210219.0.bz2',  # GISCE
        ]
        self.b5d_filenames = [
            'B5D_4321_1234_20170507.0',  # Documented
            'B5D_0189_0373_20210219.0.bz2',  # GISCE
        ]
        self.rf5d_filenames = [
            'RF5D_0237_0762_20211008.0',  # Documented
        ]
        self.mhcil_filenames = [
            'MHCIL_H2_4444_A1_20211201.0'  # Documented
        ]
        self.medidas_filenames = [
            'medidas_1234_202402_2_20240301.zip',  # Documented
            'medidas_1234_5678_202402_2_20240301.zip'  # Documented
        ]
        self.corbagen_filenames = [
            'CORBAGEN_202403.0'  # Documented
        ]
        self.wrong_filename = 'P1_20170507_20170706.6'
        self.infpa_filenames = [
            'INFPA_H3_1234_P2_202401.0.bz2'  # Documented
        ]

    with it('test to get EPFPF parser'):
        for filename in self.epfpf_filenames:
            expect(get_parser(filename)).to(equal(EPFPF))
    with it('EPFPF parser fits file format'):
        with PackedCchFile('spec/curve_files/EPFPF_HD_GEN_1234_P1_20200201.1.bz2') as packed:
            for cch_file in packed:
                for line in cch_file:
                    expected_epfpf = 'ES1234000000000001JN0F;2021;02;01;12;AE;32;F;D;01;\n'
                    result_epfpf = line['orig']
                    assert result_epfpf == expected_epfpf
                    break
                break

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

    with it('test to get A5D parser'):
        for filename in self.a5d_filenames:
            expect(get_parser(filename)).to(equal(A5d))
    with it('A5D parser fits file format'):
        with PackedCchFile('spec/curve_files/A5D_0189_0373_20210219.0.bz2') as packed:
            for cch_file in packed:
                for line in cch_file:
                    expected_a5d = 'ES0189000048220011CR0F;2021/01/01 01:00;0;0;;;;;;;;M21040709;\n'
                    result_a5d = line['orig']
                    assert result_a5d == expected_a5d
                    break
                break

    with it('test to get B5D parser'):
        for filename in self.b5d_filenames:
            expect(get_parser(filename)).to(equal(B5d))
    with it('B5D parser fits file format'):
        with PackedCchFile('spec/curve_files/B5D_0189_0373_20210219.0.bz2') as packed:
            for cch_file in packed:
                for line in cch_file:
                    expected_b5d = 'ES0189000048220011CR0F;2021/01/01 01:00;0;0;0;;;;;;;M21040709;\n'
                    result_b5d = line['orig']
                    assert result_b5d == expected_b5d
                    break
                break

    with it('test to get RF5D parser'):
        for filename in self.rf5d_filenames:
            expect(get_parser(filename)).to(equal(Rf5d))
    with it('RF5D parser fits file format'):
        with CchFile('spec/curve_files/RF5D_0237_0762_20211008.0') as cch_file:
            for line in cch_file:
                expected_rf5d = 'ES0237000000130940CT0F;2021/06/01 01:00;1;189;;;;;;1;0;TA/202100018520;\r\n'
                result_rf5d = line['orig']
                assert result_rf5d == expected_rf5d
                break

    with it('test to get MHCIL parser'):
        for filename in self.mhcil_filenames:
            expect(get_parser(filename)).to(equal(Mhcil))
    with it('MHCIL parser fits file format'):
        with CchFile('spec/curve_files/MHCIL_H2_4444_A1_20211201.0') as cch_file:
            for line in cch_file:
                expected_mhcil = 'ES0044444444444444441F001;2022;01;01;00;0;0;0;0;R;\n'
                result_mhcil = line['orig']
                assert result_mhcil == expected_mhcil
                break

    with it('test to get MEDIDAS parser'):
        for filename in self.medidas_filenames:
            expect(get_parser(filename)).to(equal(Medidas))
    with it('MEDIDAS parser fits file format'):
        with PackedCchFile('spec/curve_files/medidas_1234_202402_2_20240301.zip') as packed:
            for cch_file in packed:
                for line in cch_file:
                    expected_medidas = 'ES1234000000001234561F001;2024/02/01 01:00:00;0;-24;0;0;;;R;\n'
                    result_medidas = line['orig']
                    assert result_medidas == expected_medidas
                    break
        with PackedCchFile('spec/curve_files/medidas_1234_5678_202402_2_20240301.zip') as packed:
            for cch_file in packed:
                for line in cch_file:
                    expected_medidas = 'ES1234000000001234561F001;2024/02/01 01:00:00;0;-24;0;0;;;R;\n'
                    result_medidas = line['orig']
                    assert result_medidas == expected_medidas
                    break

    with it('test to get CORBAGEN parser'):
        for filename in self.corbagen_filenames:
            expect(get_parser(filename)).to(equal(CorbaGen))
    with it('CORBAGEN parser fits file format'):
        with CchFile('spec/curve_files/CORBAGEN_202403.0') as cch_file:
            for line in cch_file:
                expected_corbagen = 'ES1234000000000001JN0F001;2024-03-01 01:00;0;0;0;0;\n'
                result_corbagen = line['orig']
                assert result_corbagen == expected_corbagen
                break

    with it('test to get INFPA parser'):
        for filename in self.infpa_filenames:
            expect(get_parser(filename)).to(equal(Infpa))
    with it('INFPA parser fits file format'):
        with PackedCchFile('spec/curve_files/INFPA_H3_1234_P2_202401.0.bz2') as packed:
            for cch_file in packed:
                for line in cch_file:
                    expected_infpa = 'ES1234000000002267QR1F001;0;20;\n'
                    result_infpa = line['orig']
                    assert result_infpa == expected_infpa
                    break

    with it('test error to get exception'):
        def test_raise_error():
            get_parser(self.wrong_filename)

        expect(test_raise_error).to(raise_error(ParserNotFoundException))
