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
# max_digit_in_multi_digit_number : what is the maximum digit that we want in the multi digit number (the one at the front of the row)
# max_answer_digit : maximum digit in the answer (e.g. if this value is 4 and max_sum=100, then max_sum really is 44 and answer can be 34, 32, etc, but not 39 for instance.)
# buffer_prefill : numbers that must be present in the final list
# use_negative : do we want to use negative numbers
# answer_can_be_negative : do we want to have exercises with negative answer
#
# NOTE: ATM it is assumed that both max_number and max_sum are positive.
def gen_numbers(how_many_numbers = 4,
                max_number = 5,
                max_sum = 15,
                first_number_digit_count = 2,
                max_digit_in_multi_digit_number = 8,
                max_answer_digit = 8,
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
    # sanitize input
    if max_answer_digit > 9 or max_answer_digit < 0:
        max_answer_digit = 9

    # if max_answer_digit > 0 then that means we want the answer to consist of
    # carefully bounded digits. We may need to re-calculate max_sum, because for
    # example if max_sum == 500, but max_answer_digit == 4, then it's immediately
    # clear that max_sum cannot be greater than 444. And even then we can't allow
    # numbers like 395 as digits 9 and 5 would violate the rule.
    if max_answer_digit > 0:
        # first find out how many digits we have in max_sum
        max_sum_digit_count = 0
        while 10 ** max_sum_digit_count < max_sum:
            max_sum_digit_count += 1

        # now find the most significant number in the max_sum
        most_significant_digit_in_max_sum = m.floor(max_sum / (10 ** (max_sum_digit_count - 1)))

        # if most_significant_digit_in_max_sum is greater than max_answer_digit,
        # then we will reduce the most_significant_digit_in_max_sum to be
        # max_answer_digit. If it is smaller though, then we need to preserve
        # it so that the resulting max_sum is something 244, instead of 444, when
        # max_answer_digit == 4 and most_significant_digit_in_max_sum == 2.
        if most_significant_digit_in_max_sum > max_answer_digit:
            # max bound of max_sum if we obey max_answer_digit
            max_bound_of_max_sum_with_digits = sum([max_answer_digit * 10 ** i for i in range(max_sum_digit_count)])
        else:
            max_bound_of_max_sum_with_digits = most_significant_digit_in_max_sum * 10 ** (max_sum_digit_count - 1)
            max_bound_of_max_sum_with_digits += sum([max_answer_digit * 10 ** i for i in range(max_sum_digit_count - 1)])

        if max_sum > max_bound_of_max_sum_with_digits:
            max_sum = max_bound_of_max_sum_with_digits
        # Now our max_sum will be something like 444 if max_answer_digit = 4 and initial max_sum was greater than 444.
        # Or something like 244 if max_sum was only something like 299. But if max_sum was something like 219, then
        # we now have 219 as max_sum and of course digit 9 clearly violates the max_answer_digit rule.
        # In other ways too that doesn't guarantee that our result will obey max_answer_digit. It could be for
        # instance 349 or 299, so at the moment only the most significant digit will be strictly obeying
        # max_answer_digit rule. Let's fix that.

        # Explanation via an example: Assume that max_sum_digit_count == 3,
        # so we'll have 100's, 10's and 1's.
        # In the beginning we have max_sum, which we divide by 100. We get quotient,
        # which is the current number in max_sum moving from left to right and we
        # also get remainder, which is what we divide furhter by 10 this time.
        # That yields us the next current number in max_sum moving from left to
        # right. And finally we divide the remainder of that division by 1 and that
        # is our last digit in the max_sum. We can now compare all the digits and make
        # adjustments.
        current_digit_in_max_sum = 0
        remainder_of_max_sum = max_sum
        new_max_sum = 0
        for cnt in reversed(range(max_sum_digit_count)):
            (current_digit_in_max_sum, remainder_of_max_sum) = divmod(remainder_of_max_sum, 10 ** cnt)
            if current_digit_in_max_sum > max_answer_digit:
                new_max_sum += max_answer_digit * 10 ** cnt
            else:
                new_max_sum += current_digit_in_max_sum * 10 ** cnt

        max_sum = new_max_sum

    # if we need to have something prefilled in the buffer (e.g. to force end
    # user to use some abacus formula), then we need to make adjustments to
    # start variables to take that into account.
    if (len(buffer_prefill) > 0):
         max_sum -= sum(buffer_prefill)
         how_many_numbers -= len(buffer_prefill)

    # Generate required count of numbers
    for cnt in range(how_many_numbers):
        numbers.append(gen_non_zero(max_number, use_negative))

    # We have to make sure that our list doesn't start with a negative number.
    # For that we'll find first positive number and re-make the list so that
    # the found positive number is at the beginning.
    numbers = enforce_positive_number_first(numbers, max_number)

    # now that we have all the necessary numbers, all that's left is to
    # enforce the max_sum constraint.
    numbers = enforce_max_sum(numbers, max_number, max_answer_digit, max_sum, use_negative, answer_can_be_negative)

    # if we need a specific first number (of specific digit count), then enforcing that
    # keeping max_sum constraint (the function called will obey max_sum constraint).
    if first_number_digit_count > 0:
        numbers = enforce_given_number_first(first_number_digit_count, max_digit_in_multi_digit_number, numbers, max_number, max_sum, max_answer_digit, use_negative, answer_can_be_negative)

    # if we have to have something in the numbers list, then adding that to the
    # end of the list.
    if (len(buffer_prefill) > 0):
        for cnt in range(len(buffer_prefill)):
            numbers.append(buffer_prefill[cnt])

    return numbers

def enforce_positive_number_first(numbers=[-1,2,3], max_number = 5):
    # We have to make sure that our list doesn't start with a negative number.
    # For that we'll find first positive number and re-make the list so that
    # the found positive number is at the beginning.
    pos_loc = -1
    for cnt in range(len(numbers)):
        if numbers[cnt] > 0:
            pos_loc = cnt
            break

    if (pos_loc > -1):
        numbers = numbers[pos_loc:] + numbers[:pos_loc]
    else:
        # if there are no positive numbers at all, then make the first positive
        # and subtract from all others equally
        first_num = gen_non_zero(max_number, False)
        
        diff = first_num - numbers[0]
        numbers[0] = first_num
        
        cnt = 1
        while diff > 0:
            numbers[cnt] -= 1
            diff -= 1
            cnt += 1
            if cnt >= len(numbers): cnt = 1
        
    return numbers

#
# Will try to enforce a given first number in the list retaining max_sum constraint.
#
# first_number_digit_count : How many digits we want in the first number
# max_digit_in_multi_digit_number : what is the maximum digit in the first number
# numbers : current numbers in the row
# max_number : maximum number to use
# max_sum : maximum sum allowed for the whole row
# max_answer_digit : maximum digit in answer.
# use_negative : can we use negative numbers?
# answer_can_be_negative : can answer be negative?
#
def enforce_given_number_first(first_number_digit_count, max_digit_in_multi_digit_number = 8, numbers = [], max_number = 10, max_sum = 100, max_answer_digit = 8, use_negative = False, answer_can_be_negative = False):
    # if we want the first number to have certain number of digits, then
    # generate those digits now and try to keep enforcement of max sum.
    if (first_number_digit_count > 0):
        # sanitize input
        if max_digit_in_multi_digit_number > 9 or max_digit_in_multi_digit_number < 0:
            max_digit_in_multi_digit_number = 9

        prev_first_number = numbers[0]
        new_first_number = 0
        # we'll generate a multi-digit number, but to make sure that max_sum remains
        # enforceable, this new number needs to be less than max_sum and leave at least
        # a value of 1 (better 5) for each of the remaining numbers.
        multi_digit_number_upper_bound = max_sum - 1 * (len(numbers) - 1)

        # likewise if we have a limit on max_digit_in_multi_digit_number, then upper
        # bound is likely lower.
        multi_digit_number_upper_bound2 = sum([max_digit_in_multi_digit_number * 10 ** i for i in range(first_number_digit_count)])

        multi_digit_number_upper_bound = min(multi_digit_number_upper_bound, multi_digit_number_upper_bound2)

        # and of course the lower bound for multi-digit number must be 10 ^ (first_number_digit_count - 1)
        # so that for example if we want to generate a 3 digit number, then we generate at least 100.
        # We may want to change this in the future through a parameter.
        multi_digit_number_lower_bound = 10 ** (first_number_digit_count - 1)

        #print(multi_digit_number_lower_bound, " : ", multi_digit_number_upper_bound, " : ", len(numbers), " : ", max_sum)
        # making sure that generation will be sane.
        if (multi_digit_number_upper_bound > multi_digit_number_lower_bound):
            # making sure that it will go at least once through the cycle
            new_first_number = multi_digit_number_upper_bound + 1
            while new_first_number > multi_digit_number_upper_bound or new_first_number < multi_digit_number_lower_bound:
                new_first_number = 0
                for cnt in range(first_number_digit_count):
                    new_first_number = new_first_number * 10 + gen_non_zero(max_digit_in_multi_digit_number, False)

            numbers[0] = new_first_number

        # The first number is now with the required digit count.
        # Now we need to enforce the max_sum on this new row of numbers.
        max_sum_for_remainder_of_row = max_sum + prev_first_number - new_first_number
        numbers = numbers[:1] + enforce_max_sum(numbers[1:], max_number, max_answer_digit, max_sum_for_remainder_of_row, use_negative, answer_can_be_negative)
    return numbers

# Reduces the sum of the numbers given in numbers list by the given subtractor
# For example if we have a list of [9, 8, 7], the sum of which is 24, and
# we want to reduce that list so that the sum is 4 less, then we will end up
# with something like [7, 7, 6], giving a sum of 20.
def reduce_sum_of_numbers_by_this(numbers = [9, 8, 7], reduce_by = 4, use_negative = False):
    # To avoid eternal cycles, we'll use these vars.
    row_changed = True
    number_changed = False

    start_sum = sum(numbers) #8
    end_sum = start_sum - reduce_by # -17
    difference = reduce_by # 25

    while (difference > 0 and row_changed):
        row_changed = False
        subtractor = m.ceil(difference / len(numbers))
        for cnt in range(len(numbers)):
            number_changed = False
            # if we're not allowed to use negative numbers then make sure that we don't
            # and only optimize if difference is still there.
            if difference > 0:
                numbers[cnt] -= subtractor
                difference -= subtractor
                number_changed = True # we just changed a number at index cnt.
                
                # if we ended up with 0 and are allowed to use negative numbers, then reduce further
                # but if negative numbers are not allowed, then make it 1 and carry on.
                if (numbers[cnt] == 0):
                    if use_negative:
                        numbers[cnt] -= 1
                        difference -= 1
                    else:
                        numbers[cnt] += 1
                        difference += 1
                        # If subtractor is 1, then we've just restored the row to what was decreased before.
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

        # figure out how much is over and subtract equal share from each number in the row.
        difference = sum(numbers) - end_sum
    if difference > 0:
        print("Could not reduce sum fully. It is still ", difference, " too high.")
        
    return numbers

#
# Enforces that the sum of the given list is more than the given minimum
# numbers : current numbers
# max_number : maximum number allowed in the row
# min_sum : lower bound of the sum of the row of numbers.
def enforce_min_sum(numbers = [], max_number = 10, min_sum = 5):
    
    # control variables so that we don't get stuck in an endless loop.
    row_changed = True
    number_changed = False
    cnt = 0
    difference = min_sum - sum(numbers)
    
    # while we have difference between actual sum and minimum sum,
    # increase one number at a time.
    while difference > 0 and row_changed:
        if (numbers[cnt] < max_number):            
            numbers[cnt] += 1
            difference -= 1
            number_changed = True
            
        cnt += 1
        # if we reached the end of the row, then start from the beginning,
        # but only if we're changing anything. If there's been no number change,
        # then there's been no row change eihter and then we should stop because
        # the min sum cannot be enforced with the given constraints.
        if cnt >= len(numbers): 
            cnt = 0
            row_changed = number_changed
            number_changed = False

    # There is a chance that the enforcement was not possible. Given the
    # context of usage of this method, it is not worth raising an exception
    # and denying the output of this method. The result will already be better
    # even if full enforcement was not possible. But a warning should be issued.
    if (difference > 0):
        print("Could not enforce min sum. Sum is ", difference, " less than needed.")
        
    return numbers

#
# numbers: a row of numbers to optimize
# max_number : maximum number giving us numbers in range [-max_number, max_number]
# max_sum : maximum sum that the generated numbers must add up to
# max_answer_digit : highest digit that is allowed in the answer.
# use_negative : do we want to use negative numbers
# answer_can_be_negative : do we want to have exercises with negative answer
#
def enforce_max_sum(numbers = [], max_number = 10, max_answer_digit = 8, max_sum = 100, use_negative = False, answer_can_be_negative = False):
    # sanitize input
    if max_answer_digit > 9 or max_answer_digit < 0:
        max_answer_digit = 9

    # first let's establish the minimum bound
    if answer_can_be_negative:
        min_sum = -1 * max_sum
    else:
        min_sum = 0

    # first reduce the sum to comply with the max_sum parameter
    numbers = reduce_sum_of_numbers_by_this(numbers, sum(numbers) - max_sum, use_negative)
    # now get it above the lower bound
    numbers = enforce_min_sum(numbers, max_number, min_sum)

    # now all that's left is to enforce max_answer_digit in the answer.
    # So how much are we over if we want to enforce the max_answer_digit?
    if max_answer_digit > 0:
        # first find out what digits we have in the current sum
        cur_sum = sum(numbers)
        cur_sum_digit_count = 0
        cur_sum_digits = []
        while 10 ** cur_sum_digit_count < cur_sum:
            cur_sum_digit_count += 1

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
        current_digit_in_cur_sum = 0
        remainder_of_cur_sum = cur_sum
        for cnt in reversed(range(cur_sum_digit_count)):
            (current_digit_in_cur_sum, remainder_of_cur_sum) = divmod(remainder_of_cur_sum, 10 ** cnt)
            cur_sum_digits.append(current_digit_in_cur_sum)

        # now how much are we over?
        over_by = 0
        rev_range = [a for a in reversed(range(cur_sum_digit_count))]
        for cnt in range(cur_sum_digit_count):
            if cur_sum_digits[cnt] > max_answer_digit:
                over_by += (cur_sum_digits[cnt] - max_answer_digit * 10 ** rev_range[cnt])

    # finally reduce the whole list by what is over
    numbers = reduce_sum_of_numbers_by_this(numbers, over_by, use_negative)

    return numbers

def gen_non_zero(max_number, use_negative = False):
    # We don't normally want to generate 0-es, so if we get one, then
    # let's re-generate.
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
                max_digit_in_multi_digit_number = 8,
                max_answer_digit = 8,
                buffer_prefill = [],
                use_negative = True,
                answer_can_be_negative = False):
    for i in range(number_of_exercises):
        numbers = gen_numbers(how_many_numbers,
                            max_number,
                            max_sum,
                            first_number_digit_count,
                            max_digit_in_multi_digit_number,
                            max_answer_digit,
                            buffer_prefill,
                            use_negative,
                            answer_can_be_negative)
        print("-------------------")

        for cnt in range(len(numbers)):
            print(numbers[cnt])

        print("-------------------")
        print(sum(numbers))


#print(gen_abacus(3, 2, 4, 4, [], True, False))

#print(gen_abacus(3, 3, 200, 299, 2, 4, 4, [4], True, False))

#print(gen_abacus(3, 3, 5, 15, True, False))
#print(gen_abacus(3, 5, 7, 25, True, False))

# DONE: Rule : 2-digit number only first
# DONE: in 2 digit number both digits no more than x = [1..9]
# DONE: one of the numbers must be x
# both answer digits in a 2 digit number are no more than x
# DONE: contains x for rules like: +4 = +5 - 1 (for x = 4)
# only 1 or 2 numbers are negative
# DONE: first number is positive
# specify count of double digit numbers
