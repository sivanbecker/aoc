def solve():
    """ find the product of 3 entries that sum up to 2020"""
    input_file = "input.txt"
    input_d = {}
    input_l = []
    with open(input_file, "r") as fh:
        for l in fh:
            num = int(l.strip())
            input_d[num] = None
            input_l.append(num)
    input_l = sorted(input_l)

    for k in range(len(input_l)):
        for j in range(k + 1, len(input_l)):
            if input_l[k] + input_l[j] >= 2020:
                continue
            if 2020 - input_l[k] - input_l[j] in input_d:
                print(
                    f"N1 {2020 - input_l[k] - input_l[j]} N2 {input_l[k]} N3 {input_l[j]}"
                )
                return (2020 - input_l[k] - input_l[j]) * input_l[k] * input_l[j]


if __name__ == "__main__":
    print(solve())
