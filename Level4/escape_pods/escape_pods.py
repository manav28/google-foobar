"""
This solution uses a greeedy approach.

In the entrance state, the bunnies have two options:
1. Going to the exit directly.
2. Going to the intermediate state.

For the 1st option the sum of the values corresponding to exits gives the max value.

The 2nd option is slightly challenging. There are two key pieces of intuition.
1. The diagonal elements can be thought as "rest" positions and all bunnies arriving to that
state get added to the diagonal elements.
2. The intermediate states have cycles and it is possible to "simulate" this cycle in two halves.

Once the cycle is completed, the values in the diagonals represent the maximum number of bunnies
resting on an intermediate state in one time step.

After this, we could take the minimum of the diagonal value and the value at the corresponding
exits to calculate the number of bunnies travelling from any intermediate state to its corresponding
exit.

Complexity:
Time: O(n ^ 2)
Space: O(n ^ 2)

Where, n is the number of rooms.
The solution can be done in O(1) space if we don't need to preserve the input matrix.
"""
from copy import deepcopy


def solution(entrances, exits, path):
    """
    Calculates the maximum number of bunnies that could reach the exit.

    Args:
        entrances: A List of integers.
        exits: A list of integers.
        path: A nxn matrix of integers representing the maximum capacity of the
              path from state i to state j at each time step. i and j represent the
              row and column of the matrix respectively.

    Returns:
        An integer denoting the maximum number of bunnies able to pass the exit in one time step.
    """
    path_copy = deepcopy(path)
    max_bunnies = 0

    entrances_set = set(entrances)
    exits_set = set(exits)
    intermediates_set = set(range(len(path_copy))) - entrances_set - exits_set
    intermediates = sorted(list(intermediates_set))

    # From entrance to intermediate states
    for j in intermediates:
        for i in entrances_set:
            path_copy[j][j] += path[i][j]

    # The right upper half of the cycle in intermediate states
    for i in range(len(intermediates)-1):
        row = intermediates[i]
        for j in range(i+1, len(intermediates)):
            col = intermediates[j]
            path_copy[col][col] += min(path_copy[row][row], path_copy[row][col])

    # The left lower half of the cycle in intermediate states
    for i in range(1, len(intermediates)):
        row = intermediates[i]
        for j in range(i):
            col = intermediates[j]
            path_copy[col][col] += min(path_copy[row][row], path_copy[row][col])

    # From entrance and intermediate states to exit states
    for j in exits_set:
        for i in intermediates_set:
            max_bunnies += min(path_copy[i][j], path_copy[i][i])
            path_copy[i][i] = max(0, path_copy[i][i] - path_copy[i][j])

        for i in entrances_set:
            max_bunnies += path_copy[i][j]

    return max_bunnies
