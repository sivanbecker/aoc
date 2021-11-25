def solve():
    input_file = "input.txt"
    input_d = {}
    with open(input_file, "r") as fh:
        for l in fh:
            input_d[int(l.strip())] = None

    for k in input_d:
        if 2020 - k in input_d:
            return k * (2020 - k)


if __name__ == "__main__":
    print(solve())