from copy import deepcopy
class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.spots = [] # sum of 1's per column
        self.input = []
        self._get_input()
        self.oxygen_input = deepcopy(self.input)
        self.co2_input = deepcopy(self.input)
        self.startwith = ""

    def _get_input(self):
        for l in self._fh_iter:
            self.input.append(l)

    def fn(self, b):
        if b == '1':
            return 1
        return 0

            
    def translate_spots_to_gamma(self):
        gamma = ''
        epsilon = ''
        for e in self.spots:
            if e > len(self.input)/2:
                gamma += '1'
                epsilon += '0'
            else:
                gamma += '0'
                epsilon += '1'
        return gamma, epsilon

    def update_spots(self, st: str):
        ''' updates self.spots'''
        if len(self.spots) == 0:
            self.spots = [0]*len(st)
        for ind, _b in enumerate(st):
            self.spots[ind] += self.fn(_b)

    def input_digest(self, typ:str = None):
        inp = self.input
        if typ:
            inp = self.oxygen_input if typ == "oxygen" else self.co2_input
        for l in inp:
            self.update_spots(l)
        
    def filter_input_by_location(self, loc:int) -> None:
        if len(self.oxygen_input) > 1:
            self.spots = []
            self.input_digest(typ="oxygen")
            most_common = "1" if self.spots[loc] >= len(self.oxygen_input)/2 else "0"
            _tmp = []
            for e in self.oxygen_input:
                if e[loc] == most_common:
                    _tmp.append(e)
            self.oxygen_input = deepcopy(_tmp)

        if len(self.co2_input) > 1:
            self.spots = []
            self.input_digest(typ="co2")
            least_common = "0" if self.spots[loc] >= len(self.co2_input)/2 else "1"
            _tmp = []
            for e in self.co2_input:
                if e[loc] == least_common:
                    _tmp.append(e)
            self.co2_input = deepcopy(_tmp)


    def solve_part1(self):
        self.input_digest()
        g,e = self.translate_spots_to_gamma()
        import pudb;pu.db
        return int(g,2) * int(e,2)

    def solve_part2(self):
        location = 0
        while len(self.oxygen_input) > 1 or len(self.co2_input) > 1:
            self.filter_input_by_location(location)
            location += 1
        return int(self.oxygen_input[0],2 )*int(self.co2_input[0],2)
       