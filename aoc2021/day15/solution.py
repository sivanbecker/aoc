import networkx as nx
import numpy as np

class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.g = None
        self.ymax = None
        self.xmax = None
        self.tiles = {} # for part2

    def graph_from_input_arr(self, arr):

        def build_graph(arr):
            g = nx.DiGraph()
            # edges_list = []
            yshape, xshape = arr.shape
            self.ymax = yshape - 1
            self.xmax = xshape - 1
            for index, value in np.ndenumerate(arr):
                y,x = index
                left = (y, x-1)
                right = (y, x+1)
                up = (y-1, x)
                down = (y+1, x)
                
                for dest in (left, right, up, down):
                    if 0 <= dest[0] < yshape and 0 <= dest[1] < xshape:
                        # print(f"adding edge from {index}={value} -> {dest}={arr[dest]} with weight {arr[dest]} ")
                        g.add_edge(index, dest, weight=int(arr[dest]))
                        # edges_list.append((index, dest, int(arr[dest])))
            return g
            # self.g.add_weighted_edges_from(edges_list)
            
        self.g = build_graph(arr)

    def shortest_path(self):
        p = nx.dijkstra_path_length(self.g, (0,0), (self.ymax,self.xmax), weight='weight')
        return p

    def next_arr(self, arr):
        ''' add 1 to every elem in array but wrap around 9'''
        _arr = arr + 1
        _arr[_arr > 9] = 1
        return _arr

    def digest_input(self, part2=False):
        st = " ".join(list(next(self._fh_iter).strip()))
        _arr1 = np.fromstring(st, dtype=int, sep=" ")
        for l in self._fh_iter:
            st = " ".join(list(l.strip()))
            _arr1 = np.vstack([_arr1, np.fromstring(st, dtype=int, sep=" ")])
        return _arr1

    def generate_tiles(self):
        ''' in the case of 5X5 like in part 2, there are 9 flavours 
        of tiles (including the base tile'''
        for i in range(1, 9):
            self.tiles[i+1] = self.next_arr(self.tiles[i])
        
    def generate_big_map(self):
        ''' '''
        row1 = (self.tiles[1], self.tiles[2], self.tiles[3], self.tiles[4], self.tiles[5])
        row2 = (self.tiles[2], self.tiles[3], self.tiles[4], self.tiles[5], self.tiles[6])
        row3 = (self.tiles[3], self.tiles[4], self.tiles[5], self.tiles[6], self.tiles[7])
        row4 = (self.tiles[4], self.tiles[5], self.tiles[6], self.tiles[7], self.tiles[8])
        row5 = (self.tiles[5], self.tiles[6], self.tiles[7], self.tiles[8], self.tiles[9])

        map_r1 = np.concatenate(row1, axis=1)
        map_r2 = np.concatenate(row2, axis=1)
        map_r3 = np.concatenate(row3, axis=1)
        map_r4 = np.concatenate(row4, axis=1)
        map_r5 = np.concatenate(row5, axis=1)
        map = np.concatenate((map_r1, map_r2, map_r3, map_r4, map_r5), axis=0)
        return map

    def solve_part1(self):
        arr = self.digest_input()
        self.graph_from_input_arr(arr)
        return self.shortest_path()

    def solve_part2(self):
        self.tiles[1] = self.digest_input(part2=True)
        self.generate_tiles()
        map = self.generate_big_map()
        self.graph_from_input_arr(map)
        return self.shortest_path()