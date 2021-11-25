import re
from collections import defaultdict


class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.rules_map = {}
        self.partial_sum = {}
        self.reverse_rules_map = {}

    def _parse_rule_reverse(self, line):
        parts = line.split("bags contain")
        parent = parts[0].strip()
        subtree = {}
        leafs_lst = parts[1].strip().split(",")
        leaf_pat = re.compile("([0-9]+) (.+) bag")
        for _leaf in leafs_lst:
            leaf_mtch = leaf_pat.match(_leaf.strip())
            if leaf_mtch:
                subtree[leaf_mtch[2]] = parent
        return subtree

    def traverse_back(self, node):
        try:
            _upper_sum = self.reverse_rules_map[node]
        except KeyError:
            return set()

        try:
            for n in self.reverse_rules_map[node]:
                _upper_sum = set.union(_upper_sum, self.traverse_back(n))
        except KeyError:
            pass
        return _upper_sum

    def update_reverse_rules_map(self):
        for line in self._fh_iter:

            ret = self._parse_rule_reverse(line)

            for k in ret:

                self.reverse_rules_map[k] = self.reverse_rules_map.get(k, set())
                self.reverse_rules_map[k].add(ret[k])

    def update_rules_map(self):
        def parse_rule(line):
            parts = line.split("bags contain")
            parent = parts[0].strip()
            subtree = {parent: {}}
            leafs_lst = parts[1].strip().split(",")
            leaf_pat = re.compile("([0-9]+) (.+) bag")
            for _leaf in leafs_lst:
                leaf_mtch = leaf_pat.match(_leaf.strip())
                if leaf_mtch:
                    subtree[parent][leaf_mtch[2]] = int(leaf_mtch[1])
            return subtree

        for line in self._fh_iter:
            self.rules_map.update(parse_rule(line))

    def calc_partial_sum(self, node):
        if node in self.partial_sum:
            print(f"Already calculated {self.partial_sum[node]}")
            return self.partial_sum[node]

        if self.rules_map[node] == {}:
            self.partial_sum[node] = 1
            print(f">> {node} << is the end of the tree ")
            return 1
        part_sum = 0

        print(f"node {node} is the sum of {[(self.rules_map[node][x],x) for x in self.rules_map[node]]}")
        for x in self.rules_map[node]:
            part_sum += self.calc_partial_sum(x) * self.rules_map[node][x]

        self.partial_sum[node] = part_sum + 1   
        
        return self.partial_sum[node]
        

    def get_total_bag_sum(self, node: str) -> int:
        """ node should be a bag name like shiny gold"""
        return self.calc_partial_sum(node)

    def solve_part1(self):
        self.update_reverse_rules_map()
        return len(self.traverse_back("shiny gold"))

    def solve_part2(self):
        self.update_rules_map()
        self.calc_partial_sum("shiny gold")
        return self.partial_sum["shiny gold"] - 1 