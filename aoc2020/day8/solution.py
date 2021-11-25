class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.accum = 0
        self.curr = 1  # current instruction num
        self.insts = {}
        self.changed_inst = set()
        self.read_insts()
        self.funcs = {}

    def read_insts(self):
        counter = 1
        for line in self._fh_iter:
            self.insts[counter] = line
            counter += 1

    def curr(func):
        def wrap(*args, **kw):
            print(
                f"#: {args[0].curr} ; INST {args[0].insts[args[0].curr]} ; ACCUM {args[0].accum}"
            )
            ret = func(*args, **kw)
            print(f"#: {args[0].curr} ; ACCUM {args[0].accum}")
            return ret

        return wrap

    @curr
    def acc(self):
        self.accum += int(self.insts[self.curr].split()[1])
        del self.insts[self.curr]
        self.curr += 1

    @curr
    def jmp(self):
        old_curr = self.curr
        self.curr += int(self.insts[self.curr].split()[1])
        del self.insts[old_curr]

    @curr
    def nop(self):
        del self.insts[self.curr]
        self.curr += 1

    def digest_inst(self):
        self.funcs[self.insts[self.curr].split()[0]]()

    def solve_part1(self):
        try:
            while self.insts:
                self.digest_inst()
        except KeyError:
            return self.accum

    def solve_part2(self):
        import copy

        self.funcs["acc"] = self.acc
        self.funcs["nop"] = self.nop
        self.funcs["jmp"] = self.jmp

        while self.insts[self.curr]:
            
            if "nop" in self.insts[self.curr]:
                _tmp_insts = copy.deepcopy(self.insts)
                _tmp_curr = self.curr
                print(f"Copied state {_tmp_curr} - {_tmp_insts}")
                print(f"changing {self.insts[self.curr]} to jmp")
                self.insts[self.curr] = self.insts[self.curr].replace("nop", "jmp")
            elif "jmp" in self.insts[self.curr]:
                _tmp_insts = copy.deepcopy(self.insts)
                _tmp_curr = self.curr
                print(f"Copied state {_tmp_curr} - {_tmp_insts}")
                print(f"changing {self.insts[self.curr]} to nop")
                self.insts[self.curr] = self.insts[self.curr].replace("jmp", "nop")
            try:
                while self.insts[self.curr]:
                    self.digest_inst()
            except KeyError:
                print("reverting..")
                self.insts = _tmp_insts
                self.curr = _tmp_curr
                self.digest_inst()
        return self.accum