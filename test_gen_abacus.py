#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 22:24:58 2020

@author: arturs
"""
import unittest
from gen_abacus import enforce_positive_number_first

class TestGenAbacusMethods(unittest.TestCase):

    def test_enforce_positive_number_first(self):
        self.assertEqual(enforce_positive_number_first([-1, 2, 3], 5), [2, 3, -1])
        self.assertEqual(enforce_positive_number_first([-1, -2, 3], 5), [3, -1, -2])
        self.assertEqual(enforce_positive_number_first([-1, -2, -3], 5), [1, -3, -4])

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()