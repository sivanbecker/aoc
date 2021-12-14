from collections import defaultdict
import numpy as np
class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        
        self.fold_cmds = []
        self.arr = None

    def digest_input(self):
        largerx = 0
        largery = 0
        dots = defaultdict(bool)
        for l in self._fh_iter:
            # do something with l
            if l.strip():
                if 'fold along y=' in l:
                    self.fold_cmds.append(('y', np.flipud, int(l.strip().replace('fold along y=', ''))))
                elif 'fold along x=' in l:
                    self.fold_cmds.append(('x', np.fliplr, int(l.strip().replace('fold along x=', ''))))
                else:
                    x,y = l.strip().split(",")
                    x = int(x)
                    y=int(y)
                    dots[(y,x)] = True
                    if x > largerx:
                        largerx = x
                    if y > largery:
                        largery = y 
        print(f"LARGE X: {largerx}")
        print(f"LARGE Y: {largery}")
        self.arr = np.zeros((largery+1, largerx+1), dtype=int)
        for ax in dots:
            self.arr[ax] = 1

    def aoc_reshape(self, arr1, arr2, along):
        shape1 = arr1.shape
        shape2 = arr2.shape

        print(f"SEEMS we need a reshape {shape2} -> {shape1} after fold {along} ")
        diffy = shape1[0]-shape2[0]
        diffx = shape1[1]-shape2[1]
        if diffy:
            if diffy > 0: # arr1 is higher -> need to add lines to arr2
                newrows = np.zeros((diffy, shape2[1]), dtype=int)
                arr2 = np.vstack([arr2, newrows])
                
            else: # arr2 is higher -> need to add lines to arr1
                pass
        elif diffx:
            if diffx > 0:
                pass
            else:
                pass
        return arr1, arr2

    def fold(self, fold_once=False):
        start = self.arr
        out = self.arr
        for fold_cmd in self.fold_cmds:
            start = out
            print(fold_cmd)
            print(f"START WITH SHAPE {start.shape}")
            along, func, value = fold_cmd
            arr1 = start[:value,:] if along == "y" else start[:,:value]
            arr2 = start[value+1:,:] if along == "y" else start[:,value+1:]
            if arr1.shape != arr2.shape:
                arr1, arr2 = self.aoc_reshape(arr1, arr2, along)
            print(f"ARR1 SHAPE {arr1.shape} - ARR2 SHAPE {arr2.shape}")
            out = arr1 + func(arr2)
            if fold_once:
                return out
            print(f"AFTER {along} fold shape is {out.shape}")
        return out

    def count_visible(self, arr):
        return len(arr[arr>0])

    def visualize(self, final):
        x = final > 0
        x = x.astype(int)
        for i in range(0,x.shape[1],5):
            print("---------")
            print(x[:,i:i+5])

    def solve_part1(self):
        self.digest_input()
        return self.count_visible(self.fold(fold_once=True))
        

    def solve_part2(self):
        self.digest_input()
        self.visualize(self.fold(fold_once=False))