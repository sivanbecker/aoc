import numpy as np
class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.numbers = next(self._fh_iter).strip().split(",") # list of random input numbers
        self.boards = self.get_boards() # list of numpy boards 

    def get_boards(self):
        print("Reading input file")
        boards = []
        for l in self._fh_iter:
            if l == '':
                continue
            boards.append(self.read_single_board(self._fh_iter, first_row=l.strip().split()))
        return boards

    def read_single_board(self, fh, first_row=None):
        b = np.array(first_row)
        b = np.vstack([b, next(fh).split()])
        b = np.vstack([b, next(fh).split()])
        b = np.vstack([b, next(fh).split()])
        b = np.vstack([b, next(fh).split()])
        return b    

    def test_true_row_or_col(self, res):
        for i in range(5):
            if np.all(res[i]): # row solved
                return True
            if np.all(res[:,i]): # column solved
                return True
        return False
    def calc_winning_board_score(self, last_num, board:np.array, marked:np.array):
        return last_num * np.sum(np.where(marked == True, 0, board).astype(int))

    def mark_num_in_board(self, nums, part2=False):
        for ind, b in enumerate(self.boards):
            res = np.isin(b, nums)
            if self.test_true_row_or_col(res):
                if part2 and len(self.boards) > 1:
                    self.boards.pop(ind)
                else:
                    return int(nums[-1]), b, res

    def solve_part1(self):
        for i in range(len(self.numbers)):
            ret = self.mark_num_in_board(self.numbers[:i+1])
            if ret:
                return self.calc_winning_board_score(*ret)

    def solve_part2(self):
        for i in range(len(self.numbers)):
            ret = self.mark_num_in_board(self.numbers[:i+1], part2=True)
            if ret:
                return self.calc_winning_board_score(*ret)