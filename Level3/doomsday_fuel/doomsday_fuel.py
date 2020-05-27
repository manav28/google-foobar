"""
This solution is based on the theory of Absorbing Markov Chains.
https://en.wikipedia.org/wiki/Absorbing_Markov_chain

The question essentially asks given a matrix containing transition states and
absorbing states, what are the probablities of terminating at each absorbing state
when starting from state 0.

Once the relevant formulae are known, the solution is straightforward to implement.

Complexity:
Time: O(n ^ 3)
Space: O(n ^ 2)

Where, n is the number of states. The time complexity is dominated by the matrix
multiplication step.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from math import gcd


def solution(m):
    """
    Calculates the preobabilities of terminating at abosrbing states.

    Args:
        m: A nxn square matrix of integers representing the number of transitions
           from state i to state j. i and j represent the row and column of the matrix
           respectively.

    Returns:
        A List with numerators ND the least common multiple of the probablities.
    """
    def minor(matrix, i, j):
        """
        Calculates the minor of a matrix at a particular cell.

        Args:
            matrix: A nxn matrix.
            i: An integer denoting the row id of the cell for which minor needs to calcuclated.
            j: An integer denoting the column id of the cell for which minor needs to calcuclated.

        Returns:
            A (n-1)x(n-1) matrix representing the minor of the matrix at matrix[i][j]
        """
        return [row[:j] + row[j+1:] for k, row in enumerate(matrix) if k != i]

    def determinant(matrix):
        """
        Calculates the determinant of a matrix through a recursive process.

        Args:
            matrix: A nxn matrix.

        Returns:
            An integer denoting the determinant of the matrix.
        """
        if len(matrix) == 2:
            return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])

        return sum(((-1) ** j) * matrix[0][j] * determinant(minor(matrix, 0, j))
                   for j in range(len(matrix[0])))

    def adjoint(matrix):
        """
        Calculates the adjoint also known as the adjucate of the matrix.
        It is a matrix of cofactors for each element in the matrix.

        Args:
            matrix: A nxn matrix.

        Returns:
            A nxn matrix of cofactors for each element in the matrix
        """
        if len(matrix) == 2:
            return [[matrix[1][1], -matrix[1][0]], [-matrix[0][1], matrix[0][0]]]
        return [[((-1) ** (i+j)) * determinant(minor(matrix, i, j))
                 for j in range(len(matrix[0]))] for i in range(len(matrix))]

    def transpose(matrix):
        """
        Produces the transpose of a matrix.

        Args:
            matrix: A nxn matrix.

        Returns:
            A nxn matrix that is the transpose of the given matrix.
        """
        return list(zip(*matrix))

    def inverse(matrix):
        """
        Caclulates the inverse of a matrix with the formula,
        Inverse(matrix) = (1 / determinant(matrix)) * adjoint(matrix).

        Args:
            matrix: A nxn invertible matrix.

        Returns:
            A nxn matrrix that is the inverse of the given matrix.
        """
        det = determinant(matrix)
        adj = adjoint(matrix)
        adj_transpose = transpose(adj)
        return [[adj_transpose[i][j] / det
                 for j in range(len(adj_transpose[0]))] for i in range(len(adj_transpose))]

    def matrix_multiply(A, B):
        """
        Multiplies two matrices. The two matrices need to be valid for
        multiplication.

        Args:
            A: A mxn matrix.
            B: A nxp matrix.

        Returns:
            A mxp matrix.
        """
        result = [[0] * len(B[0]) for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def get_lcm(arr):
        """
        Calculates the least common multiple of a list of integers.

        Args:
            arr: A List of integers.

        Returns:
            An integer representing the lcm of a list of integers.
        """
        lcm = arr[0].denominator
        for frac in arr:
            lcm *= frac.denominator // gcd(frac.denominator, lcm)
        return lcm

    m_fractions = deepcopy(m)
    absorbing_states = []
    transient_states = []

    # Separating transient and absorbing states
    for i, row in enumerate(m):
        row_sum = sum(row)
        row_count = Counter(row)
        for j in range(len(m[0])):
            # Helps preserve the probability as a fraction
            m_fractions[i][j] = Fraction(
                m[i][j], row_sum) if row_sum > 0 else Fraction(0)
        if row_count[0] == len(row) or (row_count[0] == len(row) - 1 and row[i] != 0):
            absorbing_states.append(i)
        else:
            transient_states.append(i)

    R = [[0] * len(absorbing_states)
         for _ in range(len(m_fractions) - len(absorbing_states))]
    Q = [[0] * len(transient_states) for _ in range(len(transient_states))]

    i = 0
    for tr1 in transient_states:
        j = 0
        for ab1 in absorbing_states:
            R[i][j] = m_fractions[tr1][ab1]
            j += 1

        j = 0
        for tr2 in transient_states:
            # This step calculates I - Q directly
            Q[i][j] = 1 - m_fractions[tr1][tr2] if i == j else - \
                m_fractions[tr1][tr2]
            j += 1
        i += 1

    F = inverse(Q)
    prob_of_termination = matrix_multiply(F, R)

    lcm = get_lcm(prob_of_termination[0])
    result = [(prob_of_termination[0][j] *
               lcm).numerator for j in range(len(prob_of_termination[0]))]
    result.append(lcm)

    return result
