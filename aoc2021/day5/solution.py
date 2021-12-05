class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.dots = {}
        

    def test_horizontal_or_vertical(self, xstart, xend, ystart, yend):
        if xstart == xend or ystart == yend: # consider only horizontal/vertical lines
            print(f"Considering {xstart},{ystart} -> {xend},{yend}")
            return True
        return False

    def incr_dot(self, x, y):
        self.dots[(x,y)] = self.dots.get((x, y), 0) + 1

    def point_to_point(self, xstart, xend, ystart, yend):
        if xstart == xend: # horizontal
            _x = int(xstart)
            _ys = int(ystart)
            _ye = int(yend)
            if _ys < _ye:
                _range = range(_ys, _ye+1)
            else:
                _range = range(_ye, _ys+1)
            for _y in _range:
                self.incr_dot(_x,_y)

        elif ystart == yend: # vertical
            _y = int(ystart)
            _xs = int(xstart)
            _xe = int(xend)
            if _xs < _xe:
                _range = range(_xs, _xe+1)
            else:
                _range = range(_xe, _xs+1)
            for _x in _range:
                self.incr_dot(_x,_y)
        else: # diagonal
            _xs = int(xstart)
            _xe = int(xend)
            _ys = int(ystart)
            _ye = int(yend)
        
            if _xs < _xe: 
                xrange = range(_xs, _xe+1, 1)
            else:
                xrange = range(_xs, _xe-1, -1)
            if _ys < _ye: 
                yrange = range(_ys, _ye+1, 1)
            else:
                yrange = range(_ys, _ye-1, -1)    
            for _x, _y in zip(xrange, yrange):
                self.incr_dot(_x,_y)

                

    def digest_input(self, part2=False):
        for l in self._fh_iter:
            start, end = l.strip().split(" -> ")
            xstart, ystart = start.split(",")
            xend, yend = end.split(",")
            if part2:
                self.point_to_point(xstart, xend, ystart, yend)
            elif self.test_horizontal_or_vertical(xstart, xend, ystart, yend):
                self.point_to_point(xstart, xend, ystart, yend)

    def find_overlaps(self):
        c = 0
        for v in self.dots.values():
            if v>=2:
                c+=1 
        return c

    def solve_part1(self):
        self.digest_input()
        return self.find_overlaps()

    def solve_part2(self):
        self.digest_input(part2=True)
        return self.find_overlaps()