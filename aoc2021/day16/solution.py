from typing import Tuple


class Operator:

    

    
    def __init__(self, typeid, pktnum=None, bitlen=None):
        
        self.OP = {
            0: sum,
            1: '_product',
            2: min,
            3: max,
            5: '_greater_than',
            6: '_less_than',
            7: '_equal_to' 
        }
        
        self._op = self.OP[typeid]
        self._typeid = typeid
        assert bitlen or pktnum, f"Please provide pktnum or bitlen when creating new Operator Object"
        self.pktnum = pktnum # sub pkts amount (if applicable)
        self.bitlen = bitlen # sub pkts bit len (if applicable)
        self.sub_vals = []
        print(f"Initiated {self}")

    def __repr__(self):
        return f'<Operator {self._op} (PKTNUM:{self.pktnum}; BITLEN:{self.bitlen})>'

    def collect_sub_vals(self, val):
        print(f"{self} adding literal value {val}")
        self.sub_vals.append(val)
    
    def _product(self):
        from functools import reduce
        return reduce(lambda a,b: a*b ,self.sub_vals, 1)

    def _less_than(self):
        return 1 if self.sub_vals[0] < self.sub_vals[1] else 0

    def _greater_than(self):
        return 1 if self._less_than() == 0 else 0    

    def _equal_to(self):
        return 1 if self.sub_vals[0] == self.sub_vals[1] else 0

    def execute(self):
        if self._op in ('_product', '_greater_than', '_less_than', '_equal_to'):
            return self.__getattribute__(self._op)()
            # return self._product(vals=self.sub_vals)
        return self._op(self.sub_vals)
        # if self._op == 'sum':
        #     return sum(self.sub_vals)
        # if self._op == 'product':
            
            
        # if self._op == 'min':
        #     return min(self.sub_vals)
class DailyClass:

    HEX2BIN = { 
        "0":"0000",
        "1":"0001",
        "2":"0010",
        "3":"0011",
        "4":"0100",
        "5":"0101",
        "6":"0110",
        "7":"0111",
        "8":"1000",
        "9":"1001",
        "A":"1010",
        "B":"1011",
        "C":"1100",
        "D":"1101",
        "E":"1110",
        "F":"1111",
    }
    

    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.hpacket = None
        self.versions_sum = 0
        self.packet_bits = 0
        self.bits_consumed = 0

    def veradd(self, v):
        print(f"Adding version {v}")
        self.versions_sum += v

    def literal_type(self, typeid):
        ''' return True if literal pkt'''
        if typeid == 4:
            print("<< Literal PKT >> ", end='')
            return True
        else:
            print("** Operator **\n")


    def optype(self, typeid):
        ''' for different operator types '''

    def digest_input(self):
        self.hpacket = next(self._fh_iter)

    def bin_generator(self, bstring_iter):
        for bstring in bstring_iter:
            for b in bstring:
                yield b

    def get_bits_segment_and_convert(self, itr, count:int=None) -> int:
        c = count
        _bit_segment = ''
        for b in itr:
            self.bits_consumed += 1
            _bit_segment += b
            c -= 1
            if not c:
                break
        return int(_bit_segment, 2)

    def get_literal_value(self, itr):
        ''' read chunks of 5 bits and translate
        if the first bit is 1 - its not the last chunk
        if the first bit is 0 ,its the last chunk'''
        def read_chunk(itr):
            count = 5
            chunk = ''
            for b in itr:
                self.bits_consumed += 1
                chunk += b
                count -= 1
                
                if not count:
                    break
            self.packet_bits += 5
            return chunk[0] == '1', chunk[1:] 

        chunks = []
        more_to_go, chunk = read_chunk(itr)
        chunks.append(chunk)
        while more_to_go:
            more_to_go, chunk = read_chunk(itr)
            chunks.append(chunk)
        print(f"Val = {int(''.join(chunks), 2)}")
        return int(''.join(chunks), 2)

    def get_sub_pack_info(self, itr, length_type:str=None):
        print(f"I bit is {length_type}")
        if length_type == '0':
            return self.get_bits_segment_and_convert(itr, count=15), None
        elif length_type == '1':
            return None, self.get_bits_segment_and_convert(itr, count=11)

    def read_packet(self, itr):

        self.veradd(self.get_bits_segment_and_convert(itr=itr, count=3))
        typeid = self.get_bits_segment_and_convert(itr=itr, count=3)
        if self.literal_type(typeid=typeid):
            return self.get_literal_value(itr)
        else:
            
            bitlen, pktnum = self.get_sub_pack_info(itr=itr, length_type=next(itr))
            opObj = Operator(typeid, pktnum=pktnum, bitlen=bitlen)
            self.bits_consumed += 1
            if pktnum:
                print(f"Number of sub pkts is {pktnum}")
                for p in range(pktnum):
                    opObj.collect_sub_vals(self.read_packet(itr))
            else: # we got the bits length of sub packets
                start_at = self.bits_consumed
                while self.bits_consumed < start_at + bitlen: 
                    opObj.collect_sub_vals(self.read_packet(itr))
            
            return opObj.execute()

    def interpret(self):
        p2bstrings_g = map(lambda x: self.HEX2BIN[x], self.hpacket)
        bin_generator = self.bin_generator(p2bstrings_g)
        return self.read_packet(bin_generator)
        
    def solve_part1(self):
        self.digest_input()
        self.interpret()
        return self.versions_sum

    def solve_part2(self):
        self.digest_input()
        return self.interpret()