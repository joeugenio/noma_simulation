#!/usr/bin/env python3

import numpy as np
from nomalib.uppa import Pair
from nomalib.uppa import User
k = 0
def available_pairs(u):
    u.sort(reverse=True)
    pairs = []
    k = 0
    n = len(u)
    for i in range(n):
        for j in range(1+i, n):
            pairs.append(Pair(k, u[i],u[j]))
            k += 1
    return pairs


def test(users, branch):
    global k
    pairs = available_pairs(users)
    for p in pairs:
        u = users.copy()
        # print(u)
        # print(p.u1, p.u2)
        branch.append(p)
        u.remove(p.u1)
        u.remove(p.u2)
        if u != []:
            test(u, branch)
        else:
            k += 1
            # print(len(branch))
        branch.pop()
    return


branch = []
users = np.random.randint(0,50,size=20).tolist()
print(users)
print("--------------------")
test(users, branch)
print(k)
# print("--------------------")
# for p in branch:
#     print(p.u1, p.u2)

# pairs = available_pairs(users)
# for p in pairs:
#     print(p.id, p.u1, p.u2)



# pairs = all_pairs.copy()
# u = users.copy()
# stack = []

# for i in range(n_pairs):
#     pairs = available_pairs(u)
#     p = pairs[0]
#     case.append(p)
#     u.remove(p.u1)
#     u.remove(p.u2)

# print('=============')
# for c in case:
#     print(c.id, c.u1, c.u2)
# p = all_pairs[0]
# for p in all_pairs:
#     print(p.u1, p.u2)
# for p in range(all_pairs):


# pairs = available_pairs(u)
# for p in pairs:
#     print(p.u1, p.u2)





