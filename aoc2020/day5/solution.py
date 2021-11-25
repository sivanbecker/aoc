class DailyClass:

    _BOARDING_PASS_LEN = 10

    def __init__(self, bp_iter):
        """bp_iter is a file handler of the input file or the dummy_input file"""
        # self.solve()
        self.bp_iter = bp_iter
        self.seats = {}

    def solve_part1(self):
        return self.get_highest_seat()

    def solve_part2(self):
        self.get_all_seats()
        return self.find_my_seat(sorted(self.seats.keys()), self.seats)

    def get_highest_seat(self):
        self.get_all_seats()
        sorted_seats = sorted(self.seats.keys())
        return sorted_seats[-1]

    def get_all_seats(self):
        for bp in self.bp_iter:
            self.seats[self.translate_boarding_pass(bp)] = bp

    def translate_boarding_pass(self, bp):
        """ bp is boaring pass """
        assert (
            len(bp) == self._BOARDING_PASS_LEN
        ), f"Boarding pass length is different from {self._BOARDING_PASS_LEN} -> {len(bp)} {bp} "

        row = self._calc_row(bp[:7])
        col = self._calc_col(bp[7:])
        return row * 8 + col

    def _calc_row(self, row_bp):
        rows = list(range(128))
        for c in row_bp:
            if c == "F":
                rows = rows[: len(rows) // 2]

            else:
                rows = rows[len(rows) // 2 :]
        assert len(rows) == 1, f"Something went wrong with the row calculation {rows}"

        return rows[0]

    def _calc_col(self, col_bp):
        cols = list(range(8))
        for c in col_bp:

            if c == "R":
                cols = cols[len(cols) // 2 :]

            else:
                cols = cols[: len(cols) // 2]

        assert len(cols) == 1, f"Something went wrong with the cols calculation {cols}"

        return cols[0]

    def find_my_seat(self, sorted_seats, seats_dict):
        low, high = sorted_seats[0], sorted_seats[-1]
        for s in range(low, high + 1):
            if s - 1 in seats_dict and s + 1 in seats_dict and s not in seats_dict:
                return s