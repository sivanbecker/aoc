def solve(input_file):
    """ How many passwords are valid according to their policies"""

    amnt = 0
    with open(input_file, "r") as fh:
        parts = digest_lines(fh)
        validity = is_valid_pw1(parts)
        for b in validity:
            if b:
                amnt += 1
    return amnt


def digest_lines(fh):
    for line in fh:
        policy_ch, pw = line.strip().split(":")
        policy, ch = policy_ch.split()
        yield (policy, ch, pw.strip())


def is_valid_pw1(parts):
    """ for part1"""
    for policy, ch, pw in parts:
        bottom, up = policy.split("-")
        yield int(bottom) <= pw.count(ch) <= int(up)


def is_valid_pw2(parts):
    """ for part2"""
    for policy, ch, pw in parts:
        bottom, up = policy.split("-")
        yield (pw[int(bottom) - 1] + pw[int(up) - 1]).count(ch) == 1


def test_solve():
    assert solve("dummy_input.txt") == 2
    assert digest_lines(
        (
            "1-3 a: abcde",
            "1-3 b: cdefg",
            "2-9 c: ccccccccc",
        )
    )


if __name__ == "__main__":
    # input_file = "input.txt"
    input_file = "dummy_input.txt"
    print(solve(input_file))
