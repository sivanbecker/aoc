import asyncio
        
class DailyClass:

    # class Lfish:
    #     def __init__(self, timer:int = 8, max_days:int = None):
    #         self._timer = timer
    #         self.counter = 0
    #         self.max_days = max_days

    #     def __repr__(self):
    #         return f"<{self._timer}>"

    #     @property
    #     def timer(self):
    #         return self._timer
        
    #     @classmethod
    #     def create_new_fish(cls):
    #         return cls()

    #     def done(self):
    #         return self.counter > self.max_days

    #     def single_day_progress(self) -> bool:
    #         if self.done():
    #             return False

    #         self.counter += 1
    #         if self._timer == 0:
    #             self._timer = 6
    #             return True
    #         self._timer -= 1
    #         return False
            
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.population = []
        # self.population = None

    def digest_input(self):
        self.population = list(map(lambda x: int(x), next(self._fh_iter).strip().split(",")))
    # def digest_input(self, max_days:int):
    #     self.population = list(map(lambda x: self.Lfish(int(x), max_days=max_days), 
    #                             next(self._fh_iter).strip().split(",")))

    # def progress_population(self, max_days:int):
    #     day = 0

    #     while day < max_days:
    #         # if day%10 == 0:
    #         #     print(day)
    #         new_fish = []
    #         new_to_create = 0
    #         for _fish in self.population:
    #             if _fish.single_day_progress():
    #                 new_to_create += 1
    #         day += 1
    #         self.population.extend(list(map(lambda x: self.Lfish(max_days=max_days), range(new_to_create))))
    #     return len(self.population)

    def single_progress(self, index:int):
        if self.population[index] == 0:
            self.population[index] = 6
            return True
        self.population[index] -= 1
        return False

    def progress_population(self, max_days:int):
        while max_days > 0:
            print(f"{max_days}")
            max_days -=1
            new_fish = 0
            for i in range(len(self.population)):
                if self.single_progress(index=i):
                    new_fish += 1
            if new_fish:
                self.population.extend([8]*new_fish)
        return len(self.population)

    def solve_part1(self):
        max_days = 80
        self.digest_input()
        return self.progress_population(max_days=max_days)

    def solve_part2(self):
        max_days = 256
        self.digest_input()
        return asyncio.run(self.progress_population(max_days=max_days))
        