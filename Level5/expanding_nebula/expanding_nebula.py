"""Solution to the google foobar level 5 question 'Expanding Nebula'.

Here the terms image and preimage refer to function mappings.
A function (the set of rules as provided by the questions in this case) maps the
preimage to the image. That is the function when applied on the preimage yields the
image and the inverse leads to preimage (not to be confused with matrix inverse).

Transposing the given matrix reduces memory usage for the preimage choices
as the constraints given by the question has more width than height. This makes
traversing along the columns more efficient. Although we can skip the transpose step and
still traverse through columns, since python lists are row ordered, the code would
become more complex with lots of list comprehensions for slicing columns.
Furthermore, transposing doesn't affect the final result.
"""

from collections import Counter, defaultdict
from itertools import product


def solution(g):
    def get_images():
        """
        For any 2x2 tuple of booleans this function generates a dictionary
        that maps the grid to its collapsed value.

        Args:
            None.

        Returns:
            A dict with 2x2 grids as keys and either True or False as values.
            For example:
            {
                ((True, False), (False, False)): True,
                ((True, True), (False, False)): False
            }
        """
        image = {}
        for row_1 in product([True, False], repeat=2):
            for row_2 in product([True, False], repeat=2):
                key = (row_1, row_2)
                val = sum(row_1) + sum(row_2) == 1
                image[key] = val
        return image

    def get_preimages():
        """
        This is the reverse of the get_images() function.
        This function generates a tuple of 2x2 grids called preimages for
        True and False values.

        Args:
            None

        Returns:
            A dict with True and False as keys and a tuple of 2x2 grids as values.
            Here is a sample of values for both keys:
            {
                True: (((True, False), (False, False)),
                       ((False, True), (False, False))),
                False: (((True, True), (False, False))
                        ((True, True), (True, False)))
            }
        """
        pre_image = defaultdict(list)
        for key, val in IMAGES.items():
            pre_image[val].append(key)
        return pre_image

    def get_pair_choices():
        """
        This function generates all 4 possible pairs for
        True and False values.

        Args:
            None

        Returns:
            A tuple of pairs of tuples with each pair conprising of
            True or False values
        """
        return tuple(product([True, False], repeat=2))

    def transpose(matrix):
        """
        This function produces the transpose of a given matrix.

        Args:
            matrix: A 2D list of shape mxn.

        Returns:
            A 2D tuple of nxm values.
        """
        return tuple(zip(*matrix))

    def get_first_row_preimage_choices(image_row):
        """
        This function generates all possible preimages for the entire
        first row of the image.

        Args:
            image_row: A tuple of boolean values in the image of shape 1xn.

        Returns:
            A tuple of 2x(n+1) tuples representing a valid preimage for the
            entire given row of the image.
        """
        preimage_choices = PREIMAGES[image_row[0]]
        for i in range(1, len(image_row)):
            temp = []
            for preimage_choice in preimage_choices:
                for lower_row_pair in PAIR_CHOICES:
                    upper_row_pair = preimage_choice[i]
                    if IMAGES[(upper_row_pair, lower_row_pair)] == image_row[i]:
                        temp.append(preimage_choice + (lower_row_pair, ))
            preimage_choices = tuple(temp)

        return tuple([transpose(preimage) for preimage in preimage_choices])

    def get_row_preimage_choices(image_row):
        """
        This function generates all possible preimages for the entire
        given row of the image.

        Args:
            image_row: A tuple of boolean values in the image of shape 1xn.

        Returns:
            A tuple of 2x(n+1) tuples representing a valid preimage for the
            entire given row of the image.
        """
        preimage_choices = []
        for preimage_row in prev_preimage_second_row_count:
            choices = []
            for lower_row_pair in PAIR_CHOICES:
                upper_row_pair = (preimage_row[0], preimage_row[1])
                if IMAGES[(upper_row_pair, lower_row_pair)] == image_row[0]:
                    choices.append(lower_row_pair)

            for i in range(1, len(image_row)):
                temp = []
                if not choices:
                    break

                for choice in choices:
                    upper_row_pair = (preimage_row[i], preimage_row[i+1])
                    for bit in (False, True):
                        lower_row_pair = (choice[i], bit)
                        if IMAGES[(upper_row_pair, lower_row_pair)] == image_row[i]:
                            temp.append(choice + (bit, ))
                choices = temp

            for choice in choices:
                preimage_choices.append((preimage_row, choice))

        return tuple(preimage_choices)

    IMAGES = get_images()
    PREIMAGES = get_preimages()
    PAIR_CHOICES = get_pair_choices()

    g_transpose = transpose(g)
    prev_preimage_choices = get_first_row_preimage_choices(g_transpose[0])
    prev_preimage_second_row_count = Counter(
        prev_preimage_choices[i][1] for i in range(len(prev_preimage_choices)))

    for i in range(1, len(g_transpose)):
        next_preimage_second_row_count = Counter()
        next_preimage_choices = get_row_preimage_choices(g_transpose[i])

        for preimage_choice in next_preimage_choices:
            if preimage_choice[0] in prev_preimage_second_row_count:
                next_preimage_second_row_count[preimage_choice[1]
                                               ] += prev_preimage_second_row_count[preimage_choice[0]]

        prev_preimage_second_row_count = next_preimage_second_row_count

    return sum(prev_preimage_second_row_count.values())
