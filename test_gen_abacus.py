#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 22:24:58 2020

@author: arturs
"""
import unittest
from gen_abacus import gen_non_zero
from gen_abacus import reduce_sum_of_numbers_by_this
from gen_abacus import enforce_positive_number_first
from gen_abacus import enforce_min_sum
from gen_abacus import enforce_max_sum
from gen_abacus import enforce_given_number_first
from gen_abacus import gen_numbers

class TestGenAbacusMethods(unittest.TestCase):

    def test_gen_non_zero(self):
        # run it 1000 times and see that 0 never comes up
        for cnt in range(1000):
            gen_num = gen_non_zero(500, use_negative = True)
            self.assertFalse(gen_num == 0)
        
    def test_reduce_sum_of_numbers_by_this(self):
        old_row = [9, 8, 7]
        # we need a copy of old_row, because very often the passed old_row 
        # is modified in-function before returned as new_row.
        old_row_copy = [n for n in old_row]
        reduce_by = 4
        use_negative = False
        
        # Are we reducing as expected?
        new_row = reduce_sum_of_numbers_by_this(old_row, reduce_by, use_negative)
        self.assertTrue(sum(new_row) <= sum(old_row_copy) - reduce_by)
        self.assertTrue(sum(new_row) >= 0)
        
        # Are we reducing down to negative result?
        reduce_by = 25
        use_negative = True
        old_row = [9, 8, 7]
        # we need a copy of old_row, because very often the passed old_row 
        # is modified in-function before returned as new_row.
        old_row_copy = [n for n in old_row]
        new_row = reduce_sum_of_numbers_by_this(old_row, reduce_by, use_negative)
        self.assertTrue(sum(new_row) <= sum(old_row_copy) - reduce_by)
        self.assertTrue(sum(new_row) < 0)

        # Are we stopping reduction if it is impossible with given constraints
        # even if result is less than 0 (if any of given numbers was < 0)?
        old_row = [9, -8, 7]
        # we need a copy of old_row, because very often the passed old_row 
        # is modified in-function before returned as new_row.
        old_row_copy = [n for n in old_row]
        reduce_by = 25
        use_negative = False
        new_row = reduce_sum_of_numbers_by_this(old_row, reduce_by, use_negative)
        #print(sum(new_row), " <= ", sum(old_row_copy), " - ", reduce_by)
        #print(new_row, " ## ", old_row, " ## ", old_row_copy)
        self.assertTrue(sum(new_row) <= sum(old_row_copy))
        self.assertTrue(sum(new_row) < 0)
        
        # Are we stopping reduction if it is impossible with given constraints
        # leaving it at as good as we could?
        old_row = [9, 1, 7]
        # we need a copy of old_row, because very often the passed old_row 
        # is modified in-function before returned as new_row.
        old_row_copy = [n for n in old_row]
        reduce_by = 25
        use_negative = False
        new_row = reduce_sum_of_numbers_by_this(old_row, reduce_by, use_negative)
        #print(sum(new_row), " <= ", sum(old_row_copy), " - ", reduce_by)
        #print(new_row, " ## ", old_row, " ## ", old_row_copy)
        self.assertTrue(sum(new_row) <= sum(old_row_copy))
        self.assertTrue(sum(new_row) > 0)
        
    def test_enforce_positive_number_first(self):
        # testing that it moves negative numbers away from the start
        self.assertEqual(enforce_positive_number_first([-1, 2, 3], 5), [2, 3, -1])
        self.assertEqual(enforce_positive_number_first([-1, -2, 3], 5), [3, -1, -2])
        
        # testing that it generates new positive numbers correctly if the negative
        # numbers cannot be moved away from start.
        old_row = [-1, -2, -3]
        # we need a copy of old_row, because very often the passed old_row 
        # is modified in-function before returned as new_row.
        old_row_copy = [n for n in old_row]
        max_num = 5
        
        # need to test this several times to make sure that it has a chance to
        # generate enough new numbers less than max_num
        for cnt in range(100):
            old_row = [-1, -2, -3]
            old_row_copy = [n for n in old_row]
            new_row = enforce_positive_number_first(old_row, max_num)
            
            self.assertTrue(new_row[0] > 0)
            self.assertTrue(new_row[0] <= max_num)
            self.assertTrue(sum(new_row) == sum(old_row_copy))

    def test_enforce_min_sum(self):
        # first checking that it doesn't do unneccessary work
        old_row = [1, 2, 3]
        # we need a copy of old_row, because very often the passed old_row 
        # is modified in-function before returned as new_row.
        old_row_copy = [n for n in old_row]
        max_number = 10
        min_sum = 6
        
        new_row = enforce_min_sum(old_row, max_number, min_sum)
        self.assertEqual(old_row_copy, new_row)
        
        # now that it changes the row correctly:
        # Is it going to increase all numbers to max?
        max_number = 10
        min_sum = 30

        old_row = [1, 2, 3]
        # we need a copy of old_row, because very often the passed old_row 
        # is modified in-function before returned as new_row.
        old_row_copy = [n for n in old_row]
        
        new_row = enforce_min_sum(old_row, max_number, min_sum)
        self.assertEqual(sum(new_row), min_sum)
        self.assertEqual(len(new_row), len(old_row_copy))
        
        # What does it do when it can't achieve the goal? It should do as good
        # as it can and print out a warning.
        max_number = 10
        min_sum = 31

        old_row = [1, 2, 3]
        # we need a copy of old_row, because very often the passed old_row 
        # is modified in-function before returned as new_row.
        old_row_copy = [n for n in old_row]
        
        new_row = enforce_min_sum(old_row, max_number, min_sum)
        self.assertEqual(sum(new_row), min_sum - 1)
        self.assertEqual(len(new_row), len(old_row_copy))
        
    def test_enforce_max_sum(self):
        # first do we do unnecessary work?
        old_row = [1, 2, 3]
        # we need a copy of old_row, because very often the passed old_row 
        # is modified in-function before returned as new_row.
        old_row_copy = [n for n in old_row]
        max_number = 10
        max_answer_digit = 8
        max_sum = 10
        use_negative = False
        answer_can_be_negative = False
        
        new_row = enforce_max_sum(old_row, 
                        max_number, 
                        max_answer_digit, 
                        max_sum, 
                        use_negative, 
                        answer_can_be_negative)
        
        self.assertEqual(new_row, old_row_copy)
        
        # Do we optimize?
        max_answer_digit = 8
        max_sum = 10
        old_row = [100, 200, -3]
        # we need a copy of old_row, because very often the passed old_row 
        # is modified in-function before returned as new_row.
        old_row_copy = [n for n in old_row]
        new_row = enforce_max_sum(old_row, 
                        max_number, 
                        max_answer_digit, 
                        max_sum, 
                        use_negative, 
                        answer_can_be_negative)
        #print(new_row)
        self.assertTrue(sum(new_row) <= max_sum)
        self.assertTrue(sum(new_row) >= 0)
        # because our max_sum == 10 and max_answer_digit == 8, then the whole
        # sum should be less or equal to 8
        self.assertTrue(sum(new_row) <= max_answer_digit)
        
        # Now do we optimize with negative answer?
        answer_can_be_negative = True
        old_row = [100, -200, -3]
        # we need a copy of old_row, because very often the passed old_row 
        # is modified in-function before returned as new_row.
        old_row_copy = [n for n in old_row]
        new_row = enforce_max_sum(old_row, 
                        max_number, 
                        max_answer_digit, 
                        max_sum, 
                        use_negative, 
                        answer_can_be_negative)
        self.assertTrue(sum(new_row) <= 0)
        self.assertTrue(sum(new_row) >= -max_sum)
        
    def test_enforce_given_number_first(self):
        first_number_digit_count = 1
        max_digit_in_multi_digit_number = 8
        # first checking that it doesn't do unneccessary work
        old_row = [1, 2, 3]
        # we need a copy of old_row, because very often the passed old_row 
        # is modified in-function before returned as new_row.
        old_row_copy = [n for n in old_row]
        max_number = 10
        max_sum = 100
        max_answer_digit = 8
        use_negative = False
        answer_can_be_negative = False

        # the new number is generated randomly and validated to conform to
        # the requirements. But because it's still a random number, we need
        # to test it many times.
        for cnt in range(100):
            old_row = [1, 2, 3]
            # Do we generate correctly a 1-digit-long number?
            new_row = enforce_given_number_first(first_number_digit_count, 
                                        max_digit_in_multi_digit_number, 
                                        old_row, 
                                        max_number, 
                                        max_sum, 
                                        max_answer_digit, 
                                        use_negative, 
                                        answer_can_be_negative)
       
            self.assertTrue(new_row[0] <= 8)

        # Do we generate correctly a 3-digit-long number?
        first_number_digit_count = 3
        max_number = 999
        max_sum = 1000

        # Need to check many times because we have random number generation involved.
        for cnt in range(1000):
            old_row = [1, 2, 3]
            
            new_row = enforce_given_number_first(first_number_digit_count, 
                                        max_digit_in_multi_digit_number, 
                                        old_row, 
                                        max_number, 
                                        max_sum, 
                                        max_answer_digit, 
                                        use_negative, 
                                        answer_can_be_negative)
    
            # first find out what digits we have in the first number
            first_num = new_row[0]
            cur_digit_count = 0
            cur_digits = []
            while 10 ** cur_digit_count < first_num:
                cur_digit_count += 1
    
            # Now let's split the current sum into its digits:
            #
            # Explanation via an example: Assume that cur_sum_digit_count == 3,
            # so we'll have 100's, 10's and 1's.
            # In the beginning we have cur_sum, which we divide by 100. We get quotient,
            # which is the current number in cur_sum moving from left to right and we
            # also get remainder, which is what we divide furhter by 10 this time.
            # That yields us the next current number in cur_sum moving from left to
            # right. And finally we divide the remainder of that division by 1 and that
            # is our last digit in the cur_sum. We can now compare all the digits and make
            # adjustments.
            current_digit_in_first_num = 0
            remainder_of_first_num = first_num
            for cnt in reversed(range(cur_digit_count)):
                (current_digit_in_first_num, remainder_of_first_num) = divmod(remainder_of_first_num, 10 ** cnt)
                cur_digits.append(current_digit_in_first_num)
         
            # now let's check all the digits in the resulting sum.
            for i in range(len(cur_digits)):
                self.assertTrue(cur_digits[i] <= 8)
        
    def test_gen_numbers(self):
        how_many_numbers = 4
        max_number = 5
        max_sum = 15
        first_number_digit_count = 2
        max_digit_in_multi_digit_number = 8
        max_answer_digit = 8
        buffer_prefill = []
        use_negative = True
        answer_can_be_negative = True
        
        new_row = gen_numbers(how_many_numbers,
                        max_number,
                        max_sum,
                        first_number_digit_count,
                        max_digit_in_multi_digit_number,
                        max_answer_digit,
                        buffer_prefill,
                        use_negative,
                        answer_can_be_negative)
        
        # how many numbers generated?
        self.assertEqual(len(new_row), how_many_numbers)
        #print("AAA", new_row)
        # are they all less or equal to max_number (except first one, because
        # that's a two digit number).
        for cnt in range(1, len(new_row)):
            self.assertTrue(new_row[cnt] <= max_number)
            
        # is sum less than maximum
        self.assertTrue(sum(new_row) <= max_sum)
        
        # is first number a two digit number?
        self.assertTrue(new_row[0] >= 10)
        self.assertTrue(new_row[0] <= 99)
        
if __name__ == '__main__':
    unittest.main()