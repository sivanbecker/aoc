import ast
class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.result = ''

    def digest_input(self):
        for l in self._fh_iter:
            self.add(ast.literal_eval(l))
            print(self.result)


    # def cr_test_nested_last_block(self):
    #     el = (yield)
    #     print(f"INSIDE LAST LEVEL nesting - got {el}")
    #     if isinstance(el, list) and len(el) == 2 and all(isinstance(_e, int) for _e in el):
    #         yield el[0],el[1]  # left,right regular number
    #     yield None, None
    # def cr_test_nested_block(self, count, add_left=False, add_right=False):
        
    #     el = (yield)
    #     # if add_left or add_right:
    #     #     print(f"{el} for adding left/right")
    #     print(f"INSIDE LEVEL {count} nesting - got {el}")
    #     if isinstance(el, list):
    #         for _e in el:
    #             print(f"YIELD {_e}")
    #             yield _e
    #     else:
    #         raise StopIteration(f"Got {el} which is not a list")

    def test_nested_inside_4_pairs(self, lst:list=[]):
        if lst == []:
            lst = self.result
    #     print(f"TEST NESTED IN 4 : LST={lst}")
    #     blks = {}
    #     for i in range(1,3):
    #         blks[i] = self.cr_test_nested_block(i)
    #         blks[i].__next__()
    #     blks[3] = self.cr_test_nested_last_block()
    #     blks[3].__next__()
    #     try:
    #         left,right = None, None
            
    #         for e in blks[2].send(blks[1].send(lst)):
    #             print(f"after 2 level nesting got elem {e}")
    #             left,right = blks[3].send(e)

    #         import pudb;pu.db
    #     except StopIteration:
    #         print(f"No 4 level nesting in {lst}")

        # blk1 = self.cr_test_nested_block(1)
        # blk2 = self.cr_test_nested_block(2)
        # blk3 = self.cr_test_nested_block(3)
        # blk1.__next__()
        # blk2.__next__()
        # blk3.__next__()
        # for e in blk3.send(blk2.send(blk1.send(lst))):
        #     print(f"3 level nesting elem {e}")
        
        if isinstance(lst, list):
            for lst_ind,l1 in enumerate(lst):
                # print(f"L1={l1}")
                if isinstance(l1, list):
                    for l1_ind,l2 in enumerate(l1):
                        # print(f"L2={l2}")
                        if isinstance(l2, list):
                            for l2_ind,l3 in enumerate(l2):
                                # print(f"L3={l3}")
                                if isinstance(l3, list):
                                    for l3_ind,l4 in enumerate(l3):
                                        # print(f"L4={l4}")
                                        if isinstance(l4, list) and len(l4) == 2 and isinstance(l4[0], int) and isinstance(l4[1], int):
                                            print(f" >>>>> exploding {l4}")
                                            left,right = l4
                                            # add to available left regular number
                                            if l3_ind-1 >= 0 and isinstance(l3[l3_ind-1], int):
                                                l3[l3_ind-1] += left
                                            elif l3_ind == 0 and l2_ind-1 >= 0 and isinstance(l2[l2_ind-1], int):
                                                l2[l2_ind-1] += left
                                            elif l3_ind == 0 and l2_ind == 0 and l1_ind-1 >= 0 and isinstance(l1[l1_ind-1], int):
                                                l1[l1_ind-1] += left
                                            elif l3_ind == 0 and l2_ind == 0 and l1_ind == 0 and  lst_ind-1 >= 0 and isinstance(lst[lst_ind-1], int):
                                                lst[lst_ind-1] += left
                                            # add to available right regular number
                                            if l3_ind+1 < len(l3) and isinstance(l3[l3_ind+1], int):
                                                l3[l3_ind+1] += right
                                            elif l3_ind == len(l3)-1 and l2_ind+1 < len(l2) and isinstance(l2[l2_ind+1], int):
                                                l2[l2_ind+1] += right
                                            elif l3_ind == len(l3)-1 and l2_ind == len(l2)-1 and l1_ind+1 < len(l1) and isinstance(l1[l1_ind+1], int):
                                                l1[l1_ind+1] += right
                                            elif l3_ind == len(l3)-1 and l2_ind == len(l2)-1 and l1_ind == len(l1)-1 and lst_ind+1 < len(lst) and isinstance(lst[lst_ind+1], int):
                                                lst[lst_ind+1] += right    
                                            l3[l3_ind] = 0
                                            print(f"After Exploding {l4}: {lst}")
                                        

    
    def test_10_or_greater(self):
        pass

    def reduce(self):
        ''' reduce self.result'''
        if self.test_nested_inside_4_pairs():
            pass
        elif self.test_10_or_greater():
            pass
        
    def add(self, num):
        ''' add num to self.result '''
        print(f"Adding {num} to {self.result}")
        self.result = [self.result, num] if self.result else num
        while self.reduce():
            pass
        
    

    def solve_part1(self):
        self.digest_input()
        return "Not Impl"

    def solve_part2(self):
        self.digest_input()
        return "Not Impl"