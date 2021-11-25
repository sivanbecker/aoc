class Day5:

    _BOARDING_PASS_LEN = 10

    def __init__(self):
        pass

    def translate_boarding_pass(self, bp):
        """ bp is boaring pass """
        assert (
            len(bp) == self._BOARDING_PASS_LEN
        ), f"Boarding pass length is different from {self._BOARDING_PASS_LEN} -> {len(bp)}"

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


def test_example_cases():
    examp_cases = {
        "FBFBBFFRLR": 357,
        "BFFFBBFRRR": 567,
        "FFFBBBFRRR": 119,
        "BBFFBBFRLL": 820,
    }
    solver = Day5()
    for bp, seat in examp_cases.items():
        assert (
            solver.translate_boarding_pass(bp) == seat
        ), f"Failed translating example boading pass {bp} to {seat}"


if __name__ == "__main__":
    solver = Day5()
    seats = {}
    with open("input.txt", "r") as fh:
        for bp_line in fh:
            bp = bp_line.strip()
            seats[solver.translate_boarding_pass(bp)] = bp

    sorted_seats = sorted(seats.keys())
    print(f"Highest {sorted_seats[-1]}")
    print(f"My Seat: {solver.find_my_seat(sorted_seats, seats)}")