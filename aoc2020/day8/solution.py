import click
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
            # print(
            #     f"#: CURR {args[0].curr} ; INST {args[0].insts[args[0].curr]} ; ACCUM {args[0].accum}"
            # )
            ret = func(*args, **kw)
            # print(f"#: {args[0].curr} ; ACCUM {args[0].accum}")
            return ret

        return wrap

    @curr
    def acc(self):
        self.accum += int(self.insts[self.curr].split()[1])
        del self.insts[self.curr]
        self.curr += 1

    @curr
    def jmp(self):
        if int(self.insts[self.curr].split()[1]) == 0:
            raise ValueError("Trying to run JMP +0")
        old_curr = self.curr
        self.curr += int(self.insts[self.curr].split()[1])
        del self.insts[old_curr]

    @curr
    def nop(self):
        del self.insts[self.curr]
        self.curr += 1

    def digest_inst(self):
        # click.secho(f"Digesting {self.insts[self.curr]}", fg="red")
        # click.secho(f"BEFORE DIGEST CURR {self.curr} INSTS {self.insts} ACCUM {self.accum}", fg="green")
        self.funcs[self.insts[self.curr].split()[0]]()
        # click.secho(f"AFTER DIGEST CURR {self.curr} INSTS {self.insts} ACCUM {self.accum}", fg="blue")

    def solve_part1(self):
        self.funcs["acc"] = self.acc
        self.funcs["nop"] = self.nop
        self.funcs["jmp"] = self.jmp
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
        count = 0
        in_change = False
        last_ind = len(self.insts)
        while True:
            
            try:
                while self.curr < last_ind+1:
                    # click.secho(f"CURR {self.curr} LAST_IND {last_ind}", fg="yellow")
                    if not in_change and "nop" in self.insts[self.curr]:
                        
                        _tmp_insts = copy.deepcopy(self.insts)
                        _tmp_curr = self.curr
                        _tmp_accum = self.accum
                        # print(f"Copied state {_tmp_curr} - {_tmp_insts}")
                        # click.secho(f"changing {self.insts[self.curr]} to jmp", fg="yellow")
                        self.insts[self.curr] = self.insts[self.curr].replace("nop", "jmp")
                        in_change = True

                    elif not in_change and "jmp" in self.insts[self.curr]:
                        _tmp_insts = copy.deepcopy(self.insts)
                        _tmp_curr = self.curr
                        _tmp_accum = self.accum
                        # print(f"Copied state {_tmp_curr} - {_tmp_insts}")
                        # click.secho(f"changing {self.insts[self.curr]} to nop", fg="red")
                        self.insts[self.curr] = self.insts[self.curr].replace("jmp", "nop")
                        in_change = True
                
                    self.digest_inst()
                break
            except (KeyError, ValueError):
                # print("reverting..")
                self.insts = copy.deepcopy(_tmp_insts)
                self.curr = _tmp_curr
                self.accum=_tmp_accum 
                # print(f"State after revert {self.curr} - {self.insts}")
                self.digest_inst()
                in_change = False
        return self.accum