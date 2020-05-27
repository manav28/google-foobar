"""
Solution is self-explanatory. Just count the number of elements and return
the elements that satisfy the criteria. Python Counters maintain the order by
insertion. So the order of the original list is preserved.

Complexity:
Time - O(n)
Space - O(n)

Where, n is Number of elements in the array.
"""
from collections import Counter


def solution(data, n):
    """
    Removes duplicates that repeat more than n times.

    Args:
        data: A List of integers.
        n: An integer denoting the maximum number of repetitions.

    Returns:
        A List of integers.
    """
    if n == 0:
        return []

    count_data = Counter(data)
    return [i for i in data if count_data[i] <= n]
