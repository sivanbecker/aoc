from collections import defaultdict
class Probe:
    def __init__(self, xvel:int=None, yvel:int=None) -> None:
        self.xvel = xvel
        self.yvel = yvel
        # init position 0,0
        self.xpos = 0 
        self.ypos = 0

    def step(self):
        self.xpos += self.xvel
        self.ypos += self.yvel
        if self.xvel > 0:
            self.xvel -= 1
        elif self.xvel < 0:
            self.xvel += 1
        self.yvel -= 1
    
    def pos(self):
        # print(f"Probe current position: {self.xpos}, {self.ypos}")
        return (self.xpos, self.ypos)

class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.xtarget = None
        self.ytarget = None
        self.targets = {}
        self.highest = 0

    def digest_input(self):
        inp = next(self._fh_iter).strip()
        import re
        patst = "target area: x=(.+)\.\.(.+), y=(.+)\.\.(.+)$"
        pattern = re.compile(patst)
        m = pattern.match(inp)
        self.xtarget = (int(m[1]), int(m[2]))
        self.ytarget = (int(m[3]), int(m[4]))
        
        for x in range(self.xtarget[0], self.xtarget[1]+1):
            
            for y in range(self.ytarget[0], self.ytarget[1]+1):
                self.targets[x,y] = True

    def bulseye(self, currx, curry):
        return (currx, curry) in self.targets

    def shoot(self, x, y):
        # print(f"Shoot with {x},{y}")
        self.highest = 0
        probe = Probe(x,y)
        currx, curry = probe.pos()
        
        while (currx, curry) not in self.targets and currx < self.xtarget[1] and curry > self.ytarget[0]:
            probe.step()
            currx, curry = probe.pos()
            if curry > self.highest:
                self.highest = curry
        if self.bulseye(currx, curry):
            # print(f"{x},{y} reached {self.highest}")
            return True


    def solve_part1(self):
        self.digest_input()
        highs = defaultdict(list)
        good_vel_counter = 0
        for xvel in range(0, self.xtarget[1]):
            for yvel in range(self.ytarget[1], 500):
                # print(f"{xvel}-{yvel}")
                if self.shoot(xvel,yvel):
                    # print(f"HIGHEST = {self.highest}")
                    good_vel_counter += 1
                    highs[self.highest].append((xvel, yvel))
        highest = max(highs.keys())
        print(f"The highest was {highest}")
        return highest

    def solve_part2(self):
        self.digest_input()
        return "Not Impl"