import numpy as np
class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.octopuses = None
        self.step_flashing = {}
        self.xshape = None
        self.yshape = None
        self.flash_count = 0

    def digest_input(self):
        m = map(lambda line: list(line.strip()), self._fh_iter)
        self.octopuses = np.array(list(m), dtype=int)
        self.xshape, self.yshape = self.octopuses.shape

    def raise_if_possible(self, x ,y):
        
        if  0 <= x < self.xshape and 0 <= y < self.yshape and (x,y) not in self.step_flashing:
            # print(f"Raising E-level for {x,y} from {self.octopuses[x,y]}")
            self.octopuses[x,y] += 1
        

    def raise_surrounding(self, multi_index):
        # print(f"Raising E-level for surrounding of {multi_index}")
        x,y = multi_index
        self.raise_if_possible(x-1, y-1)
        self.raise_if_possible(x-1, y)
        self.raise_if_possible(x-1, y+1)
        self.raise_if_possible(x, y-1)
        self.raise_if_possible(x, y+1)
        self.raise_if_possible(x+1, y-1)
        self.raise_if_possible(x+1, y)
        self.raise_if_possible(x+1, y+1)

    def flash(self, multi_index):
        if multi_index in self.step_flashing:
            # print(f"Not flashing {multi_index} - already flashed this step..")
            return

        # print(f"Flashing {multi_index}")
        self.step_flashing[multi_index] = True
        self.flash_count += 1
        self.octopuses[multi_index] = 0
        self.raise_surrounding(multi_index)

    def find_flashing(self):
        if not self.octopuses[self.octopuses>9].any():
            return

        oct_iter = np.nditer(self.octopuses, flags=['multi_index'])
        for el in oct_iter:
            if el > 9:
                self.flash(oct_iter.multi_index)
        
        if self.octopuses[self.octopuses>9].any():
            self.find_flashing()

    def incr(self):
        self.octopuses += 1

    def step(self):
        self.step_flashing = {}
        self.incr()
        self.find_flashing()
        
    def run(self, count:int=None):
        steps_ran = 0
        while steps_ran < count:
            steps_ran += 1
            self.step()
            # print(f"After step {steps_ran}")
            if (self.octopuses == 0).all():
                return steps_ran

    def solve_part1(self):
        self.digest_input()
        self.run(count=100)
        return self.flash_count

    def solve_part2(self):
        self.digest_input()
        return self.run(count=2000)