from collections import defaultdict
from functools import reduce
from typing import final
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
    u = None
    m = None
    d = None 
    ru = None
    rd = None
    lu = None
    ld = None



    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.uniq_output_values = [] 
        self.seg_count_dig_options = {2: [1], 3: [7] ,4: [4], 7:[8], 5: [2,3,5], 6: [0,6,9]}
        self.digit_to_actual_segments = defaultdict(list)
        self.inputs_2 = []
        self.outputs_2 = []

    def filter_uniq(self, st):
        return len(st) in (2,3,4,7)

    def collect_uniq(self, out_segments):
        return list(filter(lambda st: self.filter_uniq(st), out_segments))

    def analyse_segments(self, st):
        if len(st) == 3:
            self.digit_to_actual_segments[7] = st
        elif len(st) == 2:
            self.digit_to_actual_segments[1] = st
            self.RU = list(st)
            self.RD = self.RU

        elif len(st) == 7:
            self.digit_to_actual_segments[8] = st
        elif len(st) == 4:
            self.digit_to_actual_segments[4] = st

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
        # find 6/0 (6 is like 8 without seg that exists in 1)
        for pat in inp_segments:
            if len(pat) == 6:
                for c in digits[1]:
                    if set(pat) == set(digits[8]).difference(c):     
                        digits[6] = pat
                    elif pat == digits[9]:
                        continue
                    else:
                        digits[0] = pat
        # find 5/2/3 - like 9 but without one segment
        for pat in inp_segments:
            if len(pat) == 5:
                for c in digits[1]:
                    if set(pat) == set(digits[9]).difference(c) and 5 not in digits:
                        digits[5] = pat
            if 5 in digits:
                break

        for pat in inp_segments:
            if len(pat) == 5:
                
                diff_4_1 = set(digits[4]).difference(digits[1])
                assert len(diff_4_1) == 2
                for c in diff_4_1:
                    if set(pat) == set(digits[9]).difference(c) and 3 not in digits:
                        digits[3] = pat
            if 3 in digits:
                break

        for pat in inp_segments:
            if len(pat) == 5:
                if pat != digits[5] and pat != digits[3]:
                    digits[2] = pat
        # assert all(k in digits for k in range(10))
        # assert all(v != '' for v in digits.values() )
        
        reverse_digits = {}
        for k,v in digits.items():
            reverse_digits[v] = str(k)
        import pudb;pu.db
        assert len(reverse_digits) == 9
        # for p in inp_segments:
        #     if p not in reverse_digits:
        #         reverse_digits[p] = '2'
            
        # assert len(digits) == len(reverse_digits)
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
                    # print(out_segments, final_digs)
                final_sum += int(final_digs)
                print(out_segments, final_digs)
        return final_sum
    
    def digest_input_2(self):
        for l in self._fh_iter:
            inp_segments = l.split("|")[0].split()
            out_segments = l.split("|")[1].split()
            inp_sorted = []
            out_sorted = []
            for st in inp_segments:
                inp_sorted.append(set(st))
            for st in out_segments:
                out_sorted.append(set(st))
            
            obvious = self.find_obvious(inp_sorted, out_sorted)
            if all(k in obvious for k in (1,7)):
                self.u = ''.join(set(obvious[7])-set(obvious[1]))
            if all(k in obvious for k in (1,4)): 
                self.lu = ''.join(set(obvious[4])-set(obvious[1]))   
                self.m = self.lu
                import pudb;pu.db
                
    def find_obvious(self, inp_sorted, out_sorted) -> dict:
        digits = {}
        # print(f"OUT_SORTED: {out_sorted}")
        for i in out_sorted:
            
            if len(i) == 2: 
                digits[1] = ''.join(i)
            if len(i) == 3:
                digits[7] = ''.join(i)
            if len(i) == 4:
                digits[4] = ''.join(i)
            if len(i) == 7: 
                digits[8] = ''.join(i)
        if len(digits) < 4: # need huristics since i did not convert all output to digits

            for i in inp_sorted:
                if len(i) == 2 : 
                    digits[1] = ''.join(i)
                if len(i) == 3 :
                    digits[7] = ''.join(i)
                if len(i) == 4 :
                    digits[4] = ''.join(i)
                if len(i) == 7 : 
                    digits[8] = ''.join(i)
            
            # print(list(map(lambda x: digits[''.join(x)] if ''.join(x) in digits else self.what_can_be(x, digits), out_sorted)))
        # else:
        #     print(list(map(lambda x: digits[''.join(x)] , out_sorted)))

        return digits

    def what_can_be(self, st:str, digits:dict):
        ''' just say what st can be assuming what we found so far and is saved in digits'''
        if digits:
            return self.seg_count_dig_options[len(st)]
        return "??"

    

    

    def solve_part1(self):
        self.digest_input()
        return len(self.uniq_output_values)

    def solve_part2(self):
        return self.digest_input(part2=True)
