"""
This question translates to:
What is the difference between the number of terms in a Fibonacci sequence
and number  of therms in a geometric sequence of ratio 2 so that the sum of
the terms in each sequence is less than the given value?

Complexity:
Time: O(n)
Space: O(1)

Where, n is the number of terms in the fibonacci sequence.
"""
from math import log


def solution(total_lambs):
    """
    Calculates the difference between the number of guards when being generous
    (Geometric sequence) and the number of guards when being stingy
    (Fibonacci sequence).

    Args:
        total_lambs: An integer representing the total amount of lambs available.

    Returns:
        An integer.
    """
    # Number of terms in geometric sequence
    # Example: For 7, we have 1 + 2 + 4 -> 3 terms
    generous = int(log(total_lambs+1, 2))

    # Number of terms in fibonacci sequence
    total = stingy = first = 0
    second = 1
    while total < total_lambs:
        curr = first + second
        total += curr
        first = second
        second = curr
        stingy += 1

    return stingy - generous
