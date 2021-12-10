from collections import defaultdict
from functools import reduce
class DailyClass:
    
    # 0 - 6 segments - 
    # 1 - 2 segments - (unique)
    # 2 - 5 segments -
    # 3 - 5 segments -
    # 4 - 4 segments (unique)
    # 5 - 5 segments
    # 6 - 6 segments
    # 7 - 3 segments (unique)
    # 8 - 7 segments (unique)
    # 9 - 6 segments

    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.uniq_output_values = [] 
        self.seg_count_dig_options = {2: [1], 3: [7] ,4: [4], 7:[8], 5: [2,3,5], 6: [0,6,9]}
        self.digit_to_actual_segments = defaultdict(list)

    def filter_uniq(self, st):
        return len(st) in (2,3,4,7)

    def collect_uniq(self, out_segments):
        return list(filter(lambda st: self.filter_uniq(st), out_segments))


    def disect(self):
        if all(k in self.digit_to_actual_segments for k in (1,7)):
            self.U = self.digit_to_actual_segments[7]
            for _c in self.digit_to_actual_segments[1]:
                self.U = self.U.replace(_c, '') 
        if all(k in self.digit_to_actual_segments for k in (1,4)):
            self.LU = self.digit_to_actual_segments[4]
            for _c in self.digit_to_actual_segments[1]:
                self.LU = self.LU.replace(_c, '') 
            self.LU = list(self.LU)
            self.M = self.LU

    def map_digits(self, inp_segments, out_segments):
        digits = {0: "", 1: "", 2: "", 3: "", 4: "",
                    5: "",6: "", 7: "", 8: "", 9: ""}
        line_out_uniqs = self.collect_uniq(out_segments)
        line_in_uniqs = self.collect_uniq(inp_segments)
        line_uniqs = set(line_out_uniqs + line_in_uniqs)
        for pat in line_uniqs:
            if len(pat) == 2:
                digits[1] = pat
            if len(pat) == 4:
                digits[4] = pat
            if len(pat) == 7:
                digits[8] = pat
            if len(pat) == 3:
                digits[7] = pat
        
        # find 9
        almost9 = set(digits[4]).union(set(digits[7]))
        for pat in inp_segments:
            if len(pat) == 6:
                if all(c in pat for c in almost9):
                    digits[9] = pat
            if digits[9]:
                break

        # find 6/0 (6 is like 8 without seg that exists in 1)
        for pat in inp_segments:
            if len(pat) == 6:
                for c in digits[1]:
                    if set(pat) == set(digits[8]).difference(c):     
                        digits[6] = pat
                for c in set(digits[4]).difference(digits[1]):
                    if set(pat) == set(digits[8]).difference(c):
                        digits[0] = pat
        # find 5/2/3 - like 9 but without one segment
        for pat in inp_segments:
            if len(pat) == 5:
                for c in digits[1]:
                    if set(pat) == set(digits[9]).difference(c):
                        digits[5] = pat
            if  digits[5] != '':
                break
        
        for pat in inp_segments:
            if len(pat) == 5:
                
                diff_4_1 = set(digits[4]).difference(digits[1])
                assert len(diff_4_1) == 2
                for c in diff_4_1:
                    if set(pat) == set(digits[9]).difference(c):
                        digits[3] = pat
            if digits[3] != '':
                break

        for pat in inp_segments:
            if len(pat) == 5:
                if pat != digits[5] and pat != digits[3]:
                    digits[2] = pat
        
        reverse_digits = {}
        for k,v in digits.items():
            reverse_digits[v] = str(k)

        assert len(digits) == len(reverse_digits), f"digits {len(digits)} - rev {len(reverse_digits)}"
        return reverse_digits

    def digest_input(self, part2=False):
        final_sum = 0
        for l in self._fh_iter:
            inp_segments = l.split("|")[0].split()
            out_segments = l.split("|")[1].split()
            self.uniq_output_values.extend(self.collect_uniq(out_segments))
            if part2:
                
                reverse_digits = self.map_digits(inp_segments, out_segments)
                final_digs = ''
                for p in out_segments:
                    for k in reverse_digits:
                        if set(p) == set(k):
                            final_digs += reverse_digits[k]
                final_sum += int(final_digs)
        return final_sum
    
    def solve_part1(self):
        self.digest_input()
        return len(self.uniq_output_values)

    def solve_part2(self):
        return self.digest_input(part2=True)
