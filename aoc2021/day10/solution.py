from collections import deque
class DailyClass:
    
    score = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    incomplete_score = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.score_sum = 0
        self.incomplete_score_sum = 0

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
                    return False

            if c == ">" :
                if q[-1] == "<":
                    q.pop()
                else:
                    self.score_sum += self.score[c]
                    return False

            if c == "}" :
                if q[-1] == "{":
                    q.pop()
                else:
                    self.score_sum += self.score[c]
                    return False

            if c == "]" :
                if q[-1] == "[":
                    q.pop()       
                else:
                    self.score_sum += self.score[c]
                    return False
        return True

    def complete_chunks(self, l):
        q = deque()
        for c in l:
            if (c == "]" and q[-1] == "[") or (c == "}" and q[-1] == "{") or (c == ")" and q[-1] == "(") or (c == ">" and q[-1] == "<") :
                q.pop()
            else:    
                q.append(c)
        # at this point q contains only what should be completed
        complete_str = ""
        while q:
        # for i in range(len(q),0, -1):
            c = q.pop()
            if c == "[":
                complete_str += "]"
            elif c == "{":
                complete_str += "}"
            elif c == "<":
                complete_str += ">"
            elif c == "(":
                complete_str += ")"
        completion_score = 0
        for i in range(len(complete_str)):
            completion_score = 5*completion_score + self.incomplete_score[complete_str[i]]

        return completion_score

    def digest_input(self):
        scores = []
        for l in self._fh_iter:
            # do something with l
            if self.find_first_err_in_line(l.strip()): # no errors in line
                scores.append(self.complete_chunks(l))
        return sorted(scores)[divmod(len(scores),2)[0]]

    def solve_part1(self):
        self.digest_input()
        return self.score_sum

    def solve_part2(self):
        return self.digest_input()