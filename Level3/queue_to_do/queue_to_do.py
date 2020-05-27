"""
This solution exploits the property of xor that a ^ a = 0
This property holds even if the number doesn't occur consecutively
For example, 2 ^ 4 ^ 2 = 4

Another property of use is the fact a sequence of xor's from 1 to n
has a pattern that repeats after every 4 numbers.

With these two properties, the xor between integers in the range [a, b]
can be calculated as (xor from 1 to a) xor (xor from 1 to b)

Complexity:
Time: O(n)
Space: O(1)

Where, n is the length of the range (b - a + 1).
"""


def solution(start, length):
    """
    Calculates the xor between a given range.

    Args:
        start: An integer denoting the start of the range.
        length: An integer denoting the length of the range.

    Returns:
        An integer.
    """
    def get_xor(end):
        end = max(0, end)
        xor_dict = {0: end, 1: 1, 2: end+1, 3: 0}
        return xor_dict[end % 4]

    check_sum = 0
    for i in reversed(range(length)):
        check_sum ^= (get_xor(start-1) ^ get_xor(start+i))
        start += length

    return check_sum
