from collections import deque
from typing import Tuple
import itertools

class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.preamble_len = None
        self.numbers = deque()

    def set_preamble(self, preamble_len: int = 0):
        assert preamble_len > 0, f"Preamble length should be larger then 0 but i got {preamble_len}"
        self.preamble_len = preamble_len

    def is_valid_sum(self, _n: int) -> bool:
        for prenum in self.numbers:
            if _n - prenum in self.numbers:
                return True
        return False

    def look_for_contiguos_sum(self, invalid_number: int) -> Tuple[int, int]:
        sum_cache = {}
        for i in range(len(self.numbers)):
            curr_sum = self.numbers[i]
            for j in range(i+1, len(self.numbers)):
                if (i,j) not in sum_cache:
                    sum_cache[(i,j)] = curr_sum+self.numbers[j]
                curr_sum = sum_cache[(i,j)]

                # slice_sum = sum(list(itertools.islice(self.numbers, i, j+1)))
                if curr_sum > invalid_number:
                    break
                if curr_sum == invalid_number:
                    return (i,j)
                
        return (0,0)    

    def sum_smallest_largest(self, indexes):
        smallest = self.numbers[indexes[0]]
        largest = self.numbers[indexes[0]]
        for i in range(indexes[0], indexes[1]+1):
            if self.numbers[i] < smallest:
                smallest = self.numbers[i]
            if self.numbers[i] > largest:
                largest = self.numbers[i]

        return smallest + largest

    def solve_part1(self):
        self.set_preamble(25)
        counter = 0
        for _n in self._fh_iter:
            int_n = int(_n)
            if counter < self.preamble_len:
                self.numbers.append(int_n)
                counter += 1
            else:
                if self.is_valid_sum(int_n):
                    self.numbers.append(int_n)
                    self.numbers.popleft()
                else:
                    return _n



    def solve_part2(self):
        # invalid_number =127 # testcase result
        invalid_number = 144381670 # just took it part 1 solution
        for _n in self._fh_iter:
            int_n = int(_n)
            if _n != invalid_number:
                self.numbers.append(int_n)

        indexes = self.look_for_contiguos_sum(invalid_number=int(invalid_number))
        
        return str(self.sum_smallest_largest(indexes))