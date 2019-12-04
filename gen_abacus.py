#!/usr/bin/python

import random as r
import copy as c
import math as m

#
# Generates a sequence of numbers that can be then used for creating an abacus
# exercise.
#
# how_many_numbers : how many numbers to generate
# max_number : maximum giving us numbers in range [-max_number, max_number]
# max_sum : maximum sum that the generated numbers must add up to
# first_number_digit_count : how many digits we want in the first number (0 - don't care)
# buffer_prefill : numbers that must be present in the final list
# use_negative : do we want to use negative numbers
# answer_can_be_negative : do we want to have exercises with negative answer
#
# NOTE: ATM it is assumed that both max_number and max_sum are positive.
# NOTE: If we're using first_number_digit_count > 1, then that's a separate
#       number that will be added to the front of the final list. It will NOT
#       be affected by max_number constraint.
def gen_numbers(how_many_numbers = 4,
                max_number = 5,
                max_sum = 15,
                first_number_digit_count = 2,
                buffer_prefill = [],
                use_negative = True,
                answer_can_be_negative = True):
    # We'll store numbers here.
    numbers = []

    # We'll keep track of sum here to make sure that we don't exceed max_sum
    tmp_sum = 0

    # input sanity
    if max_number >= max_sum:
        max_number = max_sum - 1
    # input sanity
    if how_many_numbers <= 0:
        how_many_numbers = 1
    # input sanity
    if max_sum <= max_number:
        max_sum = max_number + 1

    # if we need to have something prefilled in the buffer (e.g. to force end
    # user to use some abacus formula), then we need to make adjustments to
    # start variables to take that into account.
    if (len(buffer_prefill) > 0):
         max_sum -= sum(buffer_prefill)
         how_many_numbers -= len(buffer_prefill)

    # Generate required count of numbers
    for cnt in range(how_many_numbers):
        numbers.append(gen_non_zero(max_number, use_negative))

    # now that we have all the necessary numbers, all that's left is to
    # enforce the max_sum constraint.
    numbers = enforce_max_sum(numbers, max_number, max_sum, use_negative, answer_can_be_negative)

    # We have to make sure that our list doesn't start with a negative number.
    # For that we'll find first positive number and re-make the list so that
    # the found positive number is at the beginning.
    numbers = enforce_positive_number_first(numbers, how_many_numbers, max_number)

    # if we want the first number to have certain number of digits, then
    # generate those digits now and try to keep enforcement of max sum.
    if (first_number_digit_count > 0):
        prev_first_number = numbers[0]
        new_first_number = 0
        for cnt in range(first_number_digit_count):
            new_first_number = new_first_number * 10 + gen_non_zero(9, False)

    # if we have to have something in the numbers list, then adding that to the
    # end of the list.
    if (len(buffer_prefill) > 0):
        for cnt in range(len(buffer_prefill)):
            numbers.append(buffer_prefill[cnt])

    return numbers

def enforce_positive_number_first(numbers=[-1,2,3], how_many_numbers = 4, max_number = 5):
    # We have to make sure that our list doesn't start with a negative number.
    # For that we'll find first positive number and re-make the list so that
    # the found positive number is at the beginning.
    pos_loc = -1
    for cnt in range(how_many_numbers):
        if numbers[cnt] > 0:
            pos_loc = cnt
            break

    if (pos_loc > -1):
        numbers = numbers[pos_loc:] + numbers[:pos_loc]
    else:
        # if there are no positive numbers at all, then make the first positive
        # and subtract from all others equally
        first_num = gen_non_zero(max_number, False)
        difference = first_num - numbers[0]
        subtractor = m.ceil(difference / (how_many_numbers - 1))
        numbers[0] = first_num
        for cnt in range(1, how_many_numbers):
            if difference > 0:
                numbers[cnt] -= subtractor
                difference -= subtractor
    return numbers

#
# Will try to enforce a given first number in the list retaining max_sum constraint.
#
def enforce_given_number_first(numbers=[-1,2,3], how_many_numbers = 4, max_number = 5):
    # We have to make sure that our list doesn't start with a negative number.
    # For that we'll find first positive number and re-make the list so that
    # the found positive number is at the beginning.
    pos_loc = -1
    for cnt in range(how_many_numbers):
        if numbers[cnt] > 0:
            pos_loc = cnt
            break

    if (pos_loc > -1):
        numbers = numbers[pos_loc:] + numbers[:pos_loc]
    else:
        # if there are no positive numbers at all, then make the first positive
        # and subtract from all others equally
        first_num = gen_non_zero(max_number, False)
        difference = first_num - numbers[0]
        subtractor = m.ceil(difference / (how_many_numbers - 1))
        numbers[0] = first_num
        for cnt in range(1, how_many_numbers):
            if difference > 0:
                numbers[cnt] -= subtractor
                difference -= subtractor
    return numbers

#
# numbers: a row of numbers to optimize
# max_number : maximum giving us numbers in range [-max_number, max_number]
# max_sum : maximum sum that the generated numbers must add up to
# use_negative : do we want to use negative numbers
# answer_can_be_negative : do we want to have exercises with negative answer
#
def enforce_max_sum(numbers = [], max_number = 10, max_sum = 100, use_negative = False, answer_can_be_negative = False):
    # first let's establish the minimum bound
    if answer_can_be_negative:
        min_sum = -1 * max_sum
    else:
        min_sum = 0

    # To avoid eternal cycles, we'll use these vars.
    row_changed = True
    number_changed = False

    # first get it below the uppoer bound
    while (sum(numbers) > max_sum and row_changed):
        # figure out how much is over and subtract equal share from each number in the row.
        difference = sum(numbers) - max_sum
        subtractor = m.ceil(difference / len(numbers))
        for cnt in range(len(numbers)):
            number_changed = False
            # if we're not allowed to use negative numbers then make sure that we don't
            # and only optimize if difference is still there.
            if difference > 0:
                numbers[cnt] -= subtractor
                difference -= subtractor
                number_changed = True
                # if we ended up with 0 and are allowed to use negative numbers, then reduce further
                # but if negative numbers are not allowed, then make it 1 and carry on.
                if (numbers[cnt] == 0):
                    if use_negative:
                        numbers[cnt] -= 1
                        difference -= 1
                    else:
                        numbers[cnt] += 1
                        difference += 1
                        if subtractor == 1:
                            number_changed = False
                else: # but if we ended up less than 0 and are not allowed negative numbers, then restore.
                    if (numbers[cnt] < 0 and not use_negative):
                        numbers[cnt] += subtractor
                        difference += subtractor
                        number_changed = False
            # if there were changes, then we'll need to rerun it again if we're still below threshold
            if number_changed:
                row_changed = True

    row_changed = True
    number_changed = False
    # now get it above the lower bound
    while (sum(numbers) < min_sum):
        # figure out how much is below and add equal share to each number in the row.
        difference = min_sum - sum(numbers)
        to_add = m.ceil(difference / len(numbers))
        for cnt in range(len(numbers)):
            number_changed = False
            # only make changes if difference is still there
            if difference > 0:
                numbers[cnt] += to_add
                difference -= to_add
                number_changed = True
                # if we got 0, then continue increasing
                if numbers[cnt] == 0:
                    numbers[cnt] += 1
                    difference -= 1
                # if we got more than max_number, then adjust
                if numbers[cnt] > max_number:
                    difference += numbers[cnt] - max_number
                    numbers[cnt] = max_number
                    if to_add == max_number:
                        number_changed = False

    return numbers

#
# numbers: a row of numbers to optimize
# max_number : maximum giving us numbers in range [-max_number, max_number]
# max_sum : maximum sum that the generated numbers must add up to
# use_negative : do we want to use negative numbers
# answer_can_be_negative : do we want to have exercises with negative answer
#
def enforce_max_sum(numbers = [], max_number = 10, max_sum = 100, use_negative = False, answer_can_be_negative = False):
    # now that we have all the necessary numbers, all that's left is to
    # enforce the max_sum constraint.
    g_changed = True
    while g_changed:
        g_changed = False
        changed = True
        # enforcing the sum to be less than or equal to max_sum
        while (sum(numbers) > max_sum and changed):
            changed = False
            numbers.sort()
            number_to_reduce = numbers.pop()
            if number_to_reduce > 1 or use_negative: # if it can be reduced then reduce
                changed = True
                g_changed = True
                number_to_reduce -= 1
            else:
                if number_to_reduce == 0: # if it's too small already, then re-generate it and continue the enforcement process
                    number_to_reduce = gen_non_zero(max_number, use_negative)

            numbers.append(number_to_reduce)

        # Now enforcing that sum is greater than -1 * max_sum or greater than 0
        if answer_can_be_negative:
            min_sum = -1 * max_sum
        else:
            min_sum = 0

        #print(sum(numbers), " < ", min_sum)
        while (sum(numbers) < min_sum):
            numbers.sort()
            number_to_increase = numbers.pop(0)
            g_changed = True
            number_to_increase += 1
            if (number_to_increase == 0): # if we got it to 0, then re-generate
                number_to_increase = gen_non_zero(max_number, use_negative)
            numbers.append(number_to_increase)
    return numbers

def gen_non_zero(max_number, use_negative = False):
    # We don't normally want to generate 0-es, so if we get one, then
    # let's re-generate. Also re-generate if this is the last number
    # and we're over the max_sum
    tmp_num = 0
    while tmp_num == 0:
        if use_negative:
            #print (-1 * max_number, " : ", max_number)
            tmp_num = r.randint(-1 * max_number, max_number)
        else:
            tmp_num = r.randint(1, max_number)
    return tmp_num

def gen_abacus(number_of_exercises = 3,
                how_many_numbers = 4,
                max_number = 5,
                max_sum = 15,
                first_number_digit_count = 2,
                buffer_prefill = [],
                use_negative = True,
                answer_can_be_negative = False):
    for i in range(number_of_exercises):
        numbers = gen_numbers(how_many_numbers,
                            max_number,
                            max_sum,
                            first_number_digit_count,
                            buffer_prefill,
                            use_negative,
                            answer_can_be_negative)
        print("-------------------")

        for cnt in range(len(numbers)):
            print numbers[cnt]

        print("-------------------")
        print(sum(numbers))


#print(gen_abacus(3, 2, 4, 4, [], True, False))
print(gen_abacus(3, 3, 6, 14, 2, [4], True, False))
#print(gen_abacus(3, 3, 5, 15, True, False))
#print(gen_abacus(3, 5, 7, 25, True, False))

# Rule : 2-digit number only first
# in 2 digit number both digits no more than x = [1..9]
# DONE: one of the numbers must be x
# both answer digits in a 2 digit number are no more than x
# DONE: contains x for rules like: +4 = +5 - 1 (for x = 4)
# only 1 or 2 numbers are negative
# DONE: first number is positive
# specify count of double digit numbers
