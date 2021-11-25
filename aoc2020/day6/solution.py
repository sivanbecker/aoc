class DailyClass:
    """ Day6 """

    def __init__(self, line_iter):
        self.line_iter = line_iter

    def group_iter(self):
        grp_answers = []
        for line in self.line_iter:
            if line == "":
                yield grp_answers
                grp_answers = []
            else:
                grp_answers.append(line)

        yield grp_answers

    def solve_part1(self):
        yes_count = 0
        from functools import reduce

        for grp_answers in self.group_iter():
            yes_count += len(
                reduce(
                    lambda prev_person_ans, curr_person_ans: prev_person_ans.union(
                        curr_person_ans
                    ),
                    grp_answers,
                    set(),
                )
            )
        return str(yes_count)

    def solve_part2(self):
        yes_count = 0
        from functools import reduce

        def grp_ans_iter(self):
            for grp_ans in self.group_iter():
                yield grp_ans

        def intersect_people(*x):
            return reduce(lambda a,b: set(a).intersection(set(b)), x[0])

        for grp_ans in grp_ans_iter(self):
            yes_per_group = intersect_people(grp_ans)
            yes_count += len(yes_per_group)

        return str(yes_count)