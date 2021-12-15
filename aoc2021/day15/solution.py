import networkx as nx
import numpy as np

class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.g = None

    def graph_from_input_arr(self, arr):
        for index, values in np.ndenumerate(arr):

            print(index, values)

    def digest_input(self):
        _arr = np.array(list(next(self._fh_iter).strip()), dtype=int)
        for l in self._fh_iter:
            _arr = np.vstack([_arr,list(l.strip())])
                

    def solve_part1(self):
        self.digest_input()
        return "Not Impl"

    def solve_part2(self):
        self.digest_input()
        return "Not Impl"