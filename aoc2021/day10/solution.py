from collections import deque
class DailyClass:
    
    score = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.score_sum = 0

    def find_first_err_in_line(self, l):
        q = deque()
        for c in l:
            if c in ("(", "{", "<", "["):
                q.append(c)
            if c == ")" :
                if q[-1] == "(":
                    q.pop()
                else:
                    self.score_sum += self.score[c]
                    return

            if c == ">" :
                if q[-1] == "<":
                    q.pop()
                else:
                    self.score_sum += self.score[c]
                    return

            if c == "}" :
                if q[-1] == "{":
                    q.pop()
                else:
                    self.score_sum += self.score[c]
                    return

            if c == "]" :
                if q[-1] == "[":
                    q.pop()       
                else:
                    self.score_sum += self.score[c]
                    return

    def digest_input(self):
        for l in self._fh_iter:
            # do something with l
            self.find_first_err_in_line(l.strip())

    def solve_part1(self):
        self.digest_input()
        return self.score_sum

    def solve_part2(self):
        self.digest_input()
        return "Not Impl"