"""
A recursive dynamic programming solution.
Subtracting -1 before return accomadates for an invalid solution when the
result is a combination consisting of only one term equal to n.
This happens when prev == n and rem == n.

We could have removed the -1 and included a check like

if prev == n and rem == n:
    return 0

But this is ineffecient because of an additional check in each recursive evaluation.
It is guaranteed that there will only be one such instance and it is easier to remove it
from the final result.

Complxity:
Time: O(n^2)
Space: O(n^2)

Where, n is the number of steps.
"""


def solution(n):
    """
    Calculates the number of ways in which bricks can be arranged to
    add up to n so that each step is lower than the previous one and
    the solution has atleast two steps.

    Args:
        n: An integer denoting the maximum sum of heights of steps.

    Returns:
        An integer.
    """
    def helper(prev, rem):
        """
        A recursive helper function to calculate the number of ways of
        forming the staircase.

        Args:
            prev: An integer denoting the previous height of the step.
            rem: An integer representing the sum of height remaining.

        Returns:
            An integer denoting the number of ways to form the staircase given
            a combination of (prev, rem).
        """
        if rem == 0:
            return 1

        if prev > rem:
            return 0

        if (prev, rem) in cache:
            return cache[(prev, rem)]

        cache[(prev, rem)] = helper(prev+1, rem-prev) + helper(prev+1, rem)
        return cache[(prev, rem)]

    cache = {}
    # Subtract by -1 to exclude the intance where there is only one step that is
    # equal to n. This goes against the rule of building the staircase.
    return helper(1, n) - 1
