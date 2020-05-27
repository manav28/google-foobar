"""
This solution uses the Floyd-Warshall algorithm for detecting cycles and computing
shortest paths.

Once the shortest paths are computed, running Floyd's algorithm again helps detect negative
cycles. If there is a negative cycle, we could infinitely cycle through and keep adding time
thereby saving all the bunnies.

If there is no negative cycle, we need to run a search over the state space consisting of
(vertex, path, cycle from that vertex, time limit when starting at that vertex) where the
states represent information at the point in time at which the state was added to the queue.

Vertices where time limit goes to negative (time runs out) when it reaches the end
vertex are discarded. The set of ids in the current path is yielded and compared with the
length of the maximum bunnies set.

Complexity:
Time: O(n ^ 3)
Space: O(n ^ 2)

Where, n is the number of states (rows) in the path matrix.
"""
from copy import deepcopy


def solution(times, times_limit):
    """
    Computes the set of bunnies with maximum length that are rescued.

    Args:
        times: A nxn matrix of integers representing the time taken to go from vertex i to vertex j
               where i and j are the row and column indices respectively.
        times_limit: An integer denoting the amount of time remaining for the bulkhead
                     doors to close at the start.

    Returns:
        A List containing the column ids of the bunnies that are rescued in ascending order.
    """
    def floyd(times, check_neg_cycle=False):
        """
        Floyd-Warshall algorithm for computing all pair shortest paths.

        Args:
            times: A nxn matrix of integers representing the time taken to go from vertex
                   i to vertex j where i and j are the row and column indices respectively.
            check_neg_cycle: A boolean flag to indicate whether to check for negative cycles.

        Returns:
            A nXn matrix of integers representing the shortest time taken to go from vertex i
            to vertex j where i and j are the row and column indices of the matrix respectively.
            If the check_neg_cycle is set to True, the function returns a boolean indicating
            whether a cycle was found.
        """
        n = len(times)
        shortest_times = deepcopy(times)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if shortest_times[i][k] + shortest_times[k][j] < shortest_times[i][j]:
                        if check_neg_cycle:
                            return True
                        shortest_times[i][j] = shortest_times[i][k] + \
                            shortest_times[k][j]
        return False if check_neg_cycle else shortest_times

    def get_bunnies(shortest_times, times_limit):
        """
        Performs a search over the state space of
        (vertex, path, cycle from that vertex, time limit when starting at that vertex)

        Args:
            shortest_times: A nXn matrix of integers representing the shortest time taken
                            to go from vertex i to vertex j where i and j are the row and column
                            indices of the matrix respectively.
            times_limit: An integer denoting the amount of time remaining for the bulkhead
                         doors to close at the start.

        Returns:
            None if the length of the set is equal to the number of vertices.

        Yields:
            A set of integers denoting the ids of the vertices in the current path.
        """
        n = len(shortest_times)
        start, end = 0, n - 1
        path = [start]
        # cycle_path represents the vertices of the cycle formed when starting at vertex i.
        cycle_path = [[i] for i in range(n)]
        stack = [(start, path, cycle_path, times_limit)]
        all_vertices = set(range(n))

        while stack:
            curr_vertex, curr_path, curr_cycle_path, curr_times_limit = stack.pop()
            # Exclude vertices that form a cycle starting from curr_vertex.
            for nxt in all_vertices - set(curr_cycle_path[curr_vertex]):
                time_to_nxt_from_curr = shortest_times[curr_vertex][nxt]
                time_to_curr_from_nxt = shortest_times[nxt][curr_vertex]
                nxt_cyclic_path = deepcopy(curr_cycle_path)

                if time_to_curr_from_nxt + time_to_nxt_from_curr == 0:
                    nxt_cyclic_path[curr_vertex].append(nxt)
                    nxt_cyclic_path[nxt].append(curr_vertex)

                time_to_end_from_nxt = shortest_times[nxt][end]

                if curr_times_limit - time_to_nxt_from_curr - time_to_end_from_nxt >= 0:
                    nxt_times_limit = curr_times_limit - time_to_nxt_from_curr
                    nxt_path = curr_path + [nxt]
                    stack.append(
                        (nxt, nxt_path, nxt_cyclic_path, nxt_times_limit))

                    if nxt == end:
                        bunnies = set(nxt_path)
                        yield bunnies
                        if len(bunnies) == n:
                            return

    shortest_times = floyd(times)

    has_negative_cycle = floyd(shortest_times, check_neg_cycle=True)
    if has_negative_cycle is True:
        return list(range(len(times) - 2))

    max_bunnies = set()
    for bunnies in get_bunnies(shortest_times, times_limit):
        if len(max_bunnies) < len(bunnies) or (len(max_bunnies) == len(bunnies)
                                               and sum(max_bunnies) > sum(bunnies)):
            max_bunnies = bunnies

    max_bunnies = sorted(max_bunnies - set([0, len(times) - 1]))
    return [i - 1 for i in max_bunnies]
