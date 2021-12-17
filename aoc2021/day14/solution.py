from collections import defaultdict
from copy import deepcopy
import re
from typing import Counter, Generator
import datetime
class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.template = None
        self.rules = {}
        self.count = {}
        self.memo = defaultdict(str)
        
    def digest_input(self):
        self.template = next(self._fh_iter).strip()
        next(self._fh_iter) # blank line expected
        for l in self._fh_iter:
            pair, toinsert = l.strip().split(" -> ")
            self.rules[pair] = toinsert
            self.memo[pair] = pair[0]+toinsert+pair[1]
    
    def calc_3(self, st):
        return self.memo[st[:2]][:-1]+self.memo[st[1:]]

    def step_with_mem(self, st):
        # print(f"GOT st={st}")
        if len(st) == 3:
            self.memo[st] = self.calc_3(st)
        if st in self.memo:
            print(f"using memory {st}")
            return self.memo[st]
        print(f"Not in memory {st}")

        self.memo[st] = self.step_with_mem(st[:-2])[:-1] + self.step_with_mem(st[-3:-1])[:-1] + self.step_with_mem(st[-2:])
        # print(f"inserted to memo {st}")
        return self.memo[st]

    def memoize(self, st, val):
        if st not in self.memo:
            # print(f"Memoizing {st} {val}")
            self.memo[st] = val

    def run_step(self, st=None) -> str:
        # print(f"RUN STEP ON {st}")
        if st is None:
            st = self.template
        if len(st) == 3:
            self.memoize(st, self.calc_3(st))

        if st =='':
            raise RuntimeError("Empty ST :(")
        if st in self.memo:
            # print(f"using memory {st}")
            return self.memo[st]
        if st in self.rules:
            return self.rules[st]
        # separate into 3 parts (halves + one pair in the middle)
        stlen = len(st)
        half_len = int(stlen/2)
        p1 = st[:half_len]
        p2 = st[half_len-1:half_len+1]
        p3 = st[half_len:]
        # print(f"P1 {p1} ; P2 {p2} ; P3 {p3}")
        self.memoize(p1, self.run_step(p1))
        self.memoize(p2, self.run_step(p2))
        self.memoize(p3, self.run_step(p3))
        self.memoize(st, self.memo[p1][:-1] + self.memo[p2][:-1] + self.memo[p3])
        return self.memo[st]

    def run1(self, steps:int = 0) -> str:
        # st = deepcopy(self.template)
        while steps:
            self.template = self.run_step(self.template)
            steps -=1
        return self.template

    def run_step2(self, st: int) -> str:
        print(f"STEP on {st}")
        print(f"NCN in st {'NCN' in st}")
        if st in self.memo:
            print(f"Using value from memory ({len(st)})")
            return self.memo[st]
        self.memo[st] = self.run_step2(st[:-1])[:-1] + self.run_step2(st[-2:])
        print(f"Memorized value for {st} ({len(st)})")
        return self.memo[st]

    def run2(self, steps:int = 0) -> str:
        while steps:
            self.template = self.run_step2(self.template)
            steps -=1
        return self.template

    def solve_part1(self):
        self.digest_input()
        return self.calc_part1(self.run(steps=10))

    def solve_part2(self):
        self.digest_input()
        s = datetime.datetime.now()
        # end = self.run1(steps=30)
        print(f"Start with {self.template}")
        end = self.run2(steps=3)
        print(end)
        d = datetime.datetime.now() - s
        print(f"TOOK {d.seconds} sec")
        most_common = Counter(self.template).most_common()
        print(most_common[0][1]-most_common[-1][1])

        # print(end)
        # for i in range(40):
        #     n = self.next_poly_generator(n)
        # return self.calc_part2_1(n)
        
##############################################################

    def step2(self, lst:Generator = None) -> Generator:
        last = None
        for c in lst:
            if last:
                yield self.rules[f"{last}{c}"]
            yield c
            last = c

    def step(self, lst:Generator = None) -> Generator:
        new = ''
        for c in lst:
            print(f"adding {c}")
            if new:
                toadd = self.rules[f"{new[-1]}{c}"]
                new += toadd
                yield toadd
            new += c
            yield c 
            # if new == []: # at first new is empty
            #     new.append(c)
            # else:
            #     new.append(self.rules[f"{new[-1]}{c}"])
            #     new.append(c)
        
        # return ''.join(new)
        # yield new

    def run(self, steps:int = 0) -> str:
        ''' return final polymer string after running x steps'''
        curr = map(lambda x: x, deepcopy(self.template)) # curr is a generator

        for i in range(steps):
            print(f"STEP {i}")
            curr = self.step2(curr)

        return curr

    def calc_part1(self, polymer_str:str = None) -> int:
        ''' count most common - count least common'''
        base_elems = set(polymer_str)
        occur = {}
        for b in base_elems:
            occur[b] = len(re.findall(b, polymer_str))
        occur_sorted = sorted(occur.values())
        return occur_sorted[-1] - occur_sorted[0]

    def calc_part2(self, polymer_generator:Generator) -> int:
        from collections import defaultdict
        import time
        occur = defaultdict(int)
        for b in polymer_generator:
            # print(occur)
            occur[b] = occur.get(b, 0) + 1
        occur_sorted = sorted(occur.values())
        return occur_sorted[-1] - occur_sorted[0]
    
    def recv_st(self, func):
        import time
        print(f"initiated RECV coroutine..")
        
        while True:
            st = (yield) # st shuold be a generator , generating chars
            if not st:
                time.sleep(1)
                print(f"tralala {st}")
                continue

            new = ''
            last = ''
            
            for c in func(st):
                print(f"in {c}; last {last}")
                if last:
                    # print(f"Appending {self.rules[f'{last}{c}']}")
                    new += self.rules[f"{last}{c}"]
                # print(f"Appending {c}")
                new += c
                last = c                    
             
            self.st_gen(new)

    def st_gen(self, st):
        import time
        print(f"IN GEN {st}")
        while True:
            if not st:
                time.sleep(1)
                continue
        yield self.recv_st(st)

    def runc(self):
        print(f"start with polymer template {self.template}")
        while True:
            poly = (yield)
            # print(f"got {poly}")
            new = []
            last = ''
            for c in poly:
                print(f"in {c}; last {last}")
                if last:
                    # print(f"Appending {self.rules[f'{last}{c}']}")
                    new.append(self.rules[f"{last}{c}"])
                # print(f"Appending {c}")
                new.append(c)
                last = c                    
            yield new

    def next_poly_generator(self, curr):
        d = defaultdict(int)
        last = ''
        for c in curr:
            if last:
                _x = self.rules[f"{last}{c}"]
                yield _x
                d[_x] += 1
            yield c
            d[c] += 1
            last=c
        self.count.update(d)

    def calc_part2_1(self, p):
        from collections import Counter
        res = Counter(p)
        k = res.most_common()
        # res = max(res, key = res.get)
        return k

