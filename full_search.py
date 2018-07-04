#!/usr/bin/env python3

import numpy as np
from nomalib.uppa import Pair
from nomalib.uppa import User

class BestPair:
    ''' Class for search best pair for exahustive search '''
    def __init__(self, thr_func):
        self.thr_func = thr_func
        self.branch = []
        self.all_pairs = []

    def available_pairs(self, u):
        u.sort(reverse=True)
        pairs = []
        k = 0
        n = len(u)
        for i in range(n):
            for j in range(1+i, n):
                pairs.append(Pair(k, u[i],u[j]))
                k += 1
        return pairs

    def pairs_test(self, users):
        pairs = self.available_pairs(users)
        for p in pairs:
            u = users.copy()
            self.branch.append(p)
            u.remove(p.u1)
            u.remove(p.u2)
            if u != []:
                self.pairs_test(u)
            else:
                self.all_pairs.append(self.branch.copy())
            self.branch.pop()
        return

    def search_best_pairs(self, users):
        print(users)
        print("--------------------")
        self.pairs_test(users)
        thr_max = 0
        best_pair = None
        print(len(self.all_pairs))
        print(self.all_pairs)
        for pairs in self.all_pairs:
            thr = []
            for p in pairs:
                thr.append(self.thr_func(p.users, 1))
            thr_cell = np.sum(thr)
            if thr_cell > thr_max:
                thr_max = thr_cell
                best_pair = pairs
        return (best_pair, thr_max)


users = np.random.randint(0,50,size=4).tolist()
b = BestPair(perf.throughput_noma)
r = b.search_best_pairs(users)
# av = b.available_pairs(users)
# print(av)
# print(r[0])
# print(r[1])