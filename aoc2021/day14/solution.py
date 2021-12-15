from collections import defaultdict
from copy import deepcopy
import re
from typing import Generator
class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.template = None
        self.rules = {}
        self.count = {}

    def digest_input(self):
        self.template = next(self._fh_iter).strip()
        next(self._fh_iter) # blank line

        for l in self._fh_iter:
            # do something with l
            pair, toinsert = l.strip().split(" -> ")
            self.rules[pair] = toinsert
    
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

    def solve_part1(self):
        self.digest_input()
        return self.calc_part1(self.run(steps=10))

    def solve_part2(self):
        self.digest_input()
        n = deepcopy(self.template)
        for i in range(40):
            n = self.next_poly_generator(n)
        return self.calc_part2_1(n)
        