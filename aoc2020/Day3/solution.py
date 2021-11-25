import numpy as np
from functools import reduce


class Solve:
    def __init__(self, infile):
        self.input_file = infile
        self.trees_map_to_nparray()
        print(self.base_arr)

    def trees_map_to_nparray(self):
        self.base_arr = None
        for row in self._forest_map_rows():
            if self.base_arr is not None:
                self.base_arr = np.vstack((self.base_arr, row))
            else:
                self.base_arr = row

    def _forest_map_rows(self):
        with open(self.input_file, "r") as fh:
            for line in fh:
                yield self._line_to_list(line)

    def _line_to_list(self, line):
        return np.array(
            [c for c in line.strip().replace(".", "0").replace("#", "1")], dtype=int
        )

    def traverse(self, slope=[3, 1]):
        """slope list follows the next rule
        [right-moves, down-moves]"""
        yaxis = 0
        xaxis = 0
        tree_counter = 0
        num_rows, num_cols = self.base_arr.shape
        while yaxis < num_rows - 1:
            xaxis += slope[0]
            if xaxis >= num_cols:
                xaxis = xaxis % num_cols
            yaxis += slope[1]
            # print(f"Y {yaxis} X {xaxis}")
            tree_counter += self.base_arr[yaxis][xaxis]
        print(f"Num OF Trees: {tree_counter}")
        return tree_counter


def test_dummy():
    input_file = "dummy_input.txt"
    sl = Solve(input_file)
    assert sl.traverse([3, 1]) == 7
    assert sl.traverse([1, 1]) == 2
    assert sl.traverse([5, 1]) == 3
    assert sl.traverse([7, 1]) == 4
    assert sl.traverse([1, 2]) == 2
    assert (
        reduce(
            lambda x, y: x * y,
            map(lambda x: sl.traverse(x), ([3, 1], [1, 1], [5, 1], [7, 1], [1, 2])),
        )
        == 336
    )


if __name__ == "__main__":
    test_dummy()
    input_file = "input.txt"
    sl = Solve(input_file)
    mult = reduce(
        lambda x, y: x * y,
        map(lambda x: sl.traverse(x), ([3, 1], [1, 1], [5, 1], [7, 1], [1, 2])),
    )
    print(mult)