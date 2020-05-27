"""
The solution uses the rule for divisibility of an integer by 3:
If the sum of all digits is divisible by 3 then the number is
divisible by 3.

If not divisible by the 3, remove one or two elements. It is guaranteed
that there will be some answer after removing two elements.

Complexity:
Time: O(n^2)
Space: O(n)

Where, n is the number of elements in the array (digits).
Can be solved in O(1) space by sorting inplace.
"""


def solution(L):
    """
    Calculates the largest number divisible by 3 given an array of digits.

    Args:
        L: A List of integers denoting the digits in the number.

    Returns:
        A string that is the largest number divisible by 3.
    """
    def result_format(arr):
        arr = reversed(list(map(str, arr)))
        return "".join(arr)

    sorted_list = sorted(L)
    digit_sum = sum(sorted_list)

    if digit_sum % 3 == 0:
        return result_format(sorted_list)

    for i, num in enumerate(sorted_list):
        if (digit_sum - num) % 3 == 0:
            sorted_list.pop(i)
            return result_format(sorted_list)

    for i, num1 in enumerate(sorted_list):
        for j, num2 in enumerate(sorted_list):
            if i != j and (digit_sum - num1 - num2) % 3 == 0:
                # This order of popping is important
                sorted_list.pop(i)
                sorted_list.pop(j)
                return result_format(sorted_list)
