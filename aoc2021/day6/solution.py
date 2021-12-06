import asyncio
        
class DailyClass:

    class Lfish:
        def __init__(self, timer:int = 8, max_days:int = None):
            self._timer = timer
            self.counter = 0
            self.max_days = max_days

        def __repr__(self):
            return f"<{self._timer}>"

        @property
        def timer(self):
            return self._timer
        
        @classmethod
        def create_new_fish(cls):
            return cls()

        def done(self):
            return self.counter > self.max_days

        def single_day_progress(self) -> bool:
            if self.done():
                return False

            self.counter += 1
            if self._timer == 0:
                self._timer = 6
                return True
            self._timer -= 1
            return False
            
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.population = None

    def digest_input(self, max_days:int):
        self.population = list(map(lambda x: self.Lfish(int(x), max_days=max_days), 
                                next(self._fh_iter).strip().split(",")))

    def progress_population(self, max_days:int):
        day = 0

        while day < max_days:
            # if day%10 == 0:
            #     print(day)
            new_fishes = []
            for _fish in self.population:
                if _fish.single_day_progress():
                    new_fishes.append(self.Lfish(max_days=max_days))
            day += 1
            if new_fishes:
                self.population.extend(new_fishes)
        return len(self.population)

    def solve_part1(self):
        max_days = 80
        self.digest_input(max_days=max_days)
        return self.progress_population(max_days=max_days)

    def solve_part2(self):
        self.digest_input()
        return asyncio.run(self.progress_population(max_days=256))
        