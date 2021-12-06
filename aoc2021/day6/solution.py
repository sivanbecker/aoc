import asyncio
from collections import defaultdict        
class DailyClass:

    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.population = defaultdict(int)

    def digest_input(self):
        for _fish in next(self._fh_iter).strip().split(","):
            self.population[int(_fish)] += 1
    
    def single_progress(self, ftimer:int):
        single_end_of_day = {}
        if ftimer == 0:
            single_end_of_day[8] = self.population[0]
            single_end_of_day[6] = self.population[0]
        else:
            single_end_of_day[ftimer-1] = self.population[ftimer] 
        return single_end_of_day

    def progress_population(self, max_days:int):
        while max_days > 0:
            max_days -=1
            end_of_day_population = defaultdict(int)
            for ftimer in self.population:
                for k,v in self.single_progress(ftimer).items():
                    end_of_day_population[k] += v

            self.population = end_of_day_population
        
        return sum(self.population.values())

    def solve_part1(self):
        max_days = 80
        self.digest_input()
        return self.progress_population(max_days=max_days)

    def solve_part2(self):
        max_days = 256
        self.digest_input()
        return self.progress_population(max_days=max_days)
        