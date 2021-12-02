class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.f = 0
        self.d = 0
        self.a = 0
        
    def forward_v2(self, f):
        self.f += int(f)
        self.d += self.a * int(f)

    def forward(self, f):
        self.f += int(f)

    def down(self, d):
        self.d += int(d)

    def down_v2(self, d):
        self.a += int(d)

    def up(self, u):
        self.d -= int(u)  

    def up_v2(self, u):
        self.a -= int(u)

    def calc_position(self, part2=False):
        move = {'up': self.up_v2 if part2 else self.up, 
                "down": self.down_v2 if part2 else self.down, 
                "forward": self.forward_v2 if part2 else self.forward}

        for l in self._fh_iter:
            cmd, amount = l.strip().split()
            move[cmd](amount)
        return self.f * self.d

    def solve_part1(self):
        return self.calc_position()

    def solve_part2(self):
        return self.calc_position(part2=True)