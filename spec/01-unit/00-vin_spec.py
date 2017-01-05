#!/usr/bin/env python
# coding:utf-8

import os
import sys
import unittest

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_DIR, '../..'))

from utils.vin import Vin


class TestVin(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_wmi(self):
         vinobj = Vin("LVSHCAMB1CE054249")
         self.assertEqual(vinobj.get_wmi(), 'LVS')

    def test_get_vds(self):
         vinobj = Vin("LVSHCAMB1CE054249")
         self.assertEqual(vinobj.get_vds(), 'HCAMB')

    def test_get_year(self):
         vinobj = Vin("LVSHCAMB1CE054249")
         self.assertEqual(vinobj.get_year(), 'C')

    def test_get_checksum(self):
         vinobj = Vin("LVSHCAMB1CE054249")
         self.assertEqual(vinobj.get_checksum(), '1')

    def test_is_valid_00(self):
         vinobj = Vin("LVSHCAMB1CE054249")
         self.assertEqual(vinobj.is_valid(), True)

    def test_is_valid_01(self):
         vinobj = Vin("LVSHCAMB1CE0542490")
         self.assertEqual(vinobj.is_valid(), False)

    def test_is_valid_02(self):
         vinobj = Vin("LVSHCAMB1CE05424I")
         self.assertEqual(vinobj.is_valid(), False)

    def test_is_valid_03(self):
         vinobj = Vin("LVSHCAMB1CE05424O")
         self.assertEqual(vinobj.is_valid(), False)

    def test_is_valid_04(self):
         vinobj = Vin("LVSHCAMB1CE05424Q")
         self.assertEqual(vinobj.is_valid(), False)


if __name__ == '__main__':
        unittest.main()
