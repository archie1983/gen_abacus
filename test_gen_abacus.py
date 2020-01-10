#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 22:24:58 2020

@author: arturs
"""
import unittest
from gen_abacus import enforce_positive_number_first
from gen_abacus import enforce_min_sum

class TestGenAbacusMethods(unittest.TestCase):

    def test_enforce_positive_number_first(self):
        # testing that it moves negative numbers away from the start
        self.assertEqual(enforce_positive_number_first([-1, 2, 3], 5), [2, 3, -1])
        self.assertEqual(enforce_positive_number_first([-1, -2, 3], 5), [3, -1, -2])
        
        # testing that it generates new positive numbers correctly if the negative
        # numbers cannot be moved away from start.
        old_row = [-1, -2, -3]
        max_num = 5
        
        # need to test this several times to make sure that it has a chance to
        # generate enough new numbers less than max_num
        for cnt in range(100):
            new_row = enforce_positive_number_first(old_row, max_num)
            
            self.assertTrue(new_row[0] > 0)
            self.assertTrue(new_row[0] <= max_num)
            self.assertTrue(sum(new_row) == sum(old_row))

    def test_enforce_min_sum(self):
        # first checking that it doesn't do unneccessary work
        old_row = [1, 2, 3]
        max_number = 10
        min_sum = 6
        
        new_row = enforce_min_sum(old_row, max_number, min_sum)
        self.assertEqual(old_row, new_row)
        
        # now that it changes the row correctly:
        # Is it going to increase all numbers to max?
        max_number = 10
        min_sum = 30
        
        new_row = enforce_min_sum(old_row, max_number, min_sum)
        self.assertEqual(sum(new_row), min_sum)
        self.assertEqual(len(new_row), len(old_row))
        
        # What does it do when it can't achieve the goal? It should do as good
        # as it can and print out a warning.
        max_number = 10
        min_sum = 31
        
        new_row = enforce_min_sum(old_row, max_number, min_sum)
        self.assertEqual(sum(new_row), min_sum - 1)
        self.assertEqual(len(new_row), len(old_row))
        
    # def test_enforce_given_number_first(self):
    #     first_number_digit_count = 3
    #     max_digit_in_multi_digit_number = 8
    #     current_numbers = [1, 2, 3]
        
    #     enforce_given_number_first(first_number_digit_count, 
    #                                max_digit_in_multi_digit_number, 
    #                                current_numbers, 
    #                                max_number = 10, 
    #                                max_sum = 100, 
    #                                max_answer_digit = 8, 
    #                                use_negative = False, 
    #                                answer_can_be_negative = False)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    unittest.main()