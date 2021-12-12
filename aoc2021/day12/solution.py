import itertools
import networkx as nx
import re
from pprint import pprint
class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.g = nx.Graph()
        self.lowernodes = set()
        self.ended = 0

    def digest_input(self):
        for l in self._fh_iter:
            nodes = l.strip().split("-")
            self.g.add_edge(nodes[0], nodes[1])
            for n in nodes:
                if n.islower():
                    self.lowernodes.add(n)

    def all_combinations(self, paths:dict):
        allcomb = []
        for n in paths:
            if n == 'b':
                import pudb;pu.db
            nstart = filter(lambda x: 'end' not in x and x[0] == 'start', paths[n][0])
            nend = filter(lambda x: 'start' not in x and x[-1] == 'end', paths[n][1])
            perm = itertools.product(nstart, nend)

            for p in perm:
                allcomb.append(p[0]+p[1][1:])
        
        return allcomb

    def filter_by_condition(self, allcomb:list):
        #     ''' part 1 condition is dont pass twice in small caves'''
        filtered = []
        for comb in allcomb:
            safe = True
            s = str(comb)
            for c in self.lowernodes:
                if len(re.findall(c, s)) > 1:
                    safe = False
                    break
            if safe:
                filtered.append(comb)
    
        return filtered

    def find_all_paths(self):
        from collections import defaultdict
        paths = defaultdict(list)
        for n in self.g.nodes:
            if n == "start":
                continue
            paths[n].append(list(nx.all_simple_paths(self.g, "start", n, cutoff=200)))
            paths[n].append(list(nx.all_simple_paths(self.g, n, "end", cutoff=200)))
        
        
        toret =  self.filter_by_condition(self.all_combinations(paths))
        pprint(toret)
        return toret

    def find_all_paths2(self, origin='start', visited=None):
        if origin in self.lowernodes and visited and origin in visited:
            # print(f"already been to {origin}")
            return
        visited = visited + origin if visited else origin
        for e in self.g.edges(origin):
            # print(f"need to go from {origin} to {e[1]}")
            if origin == 'end':
                # print(f"****** reached the end {visited}")
                self.ended += 1
                return
            
            self.find_all_paths2(origin=e[1], visited=visited)
        
    def find_all_paths3(self, origin='start', visited=None):
        if origin in self.lowernodes and visited and origin in visited:
            # print(f"already been to {origin}")
            return
        visited = visited + origin if visited else origin
        for e in self.g.edges(origin):
            # print(f"need to go from {origin} to {e[1]}")
            if origin == 'end':
                # print(f"****** reached the end {visited}")
                self.ended += 1
                return
            
            self.find_all_paths2(origin=e[1], visited=visited)

    def solve_part1(self):
        self.digest_input()
        self.find_all_paths2()
        return self.ended

    def solve_part2(self):
        self.digest_input()
        return "Not Impl"