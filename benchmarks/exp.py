#!/usr/bin/env python3

"""
Example of a finite union of cubes having an exponential number of maximal
cubes. The example is directly adapted from the paper
"ON THE NUMBER OF PRIME IMPLICANTS" by Chandra and Markowsky (1978).

For simplicity, we provide the construction in the particular case where
* k is a parameter
* we write r=2^k for convenience
* The dimension (number of variables) is d=3r+k=3*2^{k}+k
* The set can be decomposed into a union of 3*r = 3*2^{k} cubes
* There are at least 3^r = 3^{2^k} maximal cubes (prime implicants in the paper)

More precisely, the example of composed of the following variables:
* a_0 ... a_{k-1} encoding 2^k blocks A_0 ... A_{2^k-1}
    (we require all blocks to be mutually exclusive and cover all possible
    valuations of the a_i's)
* b_0, c_0, d_0 to d_{2^k-1}

"""

import z3
import sys


def get_block(k, i, v):
    """Get the i-th block A_i, assuming current parameter k (0<=i<2^k)
    and list of variables v.
    """
    assert(0 <= i and i < 1<<k)
    assert(len(v) > 1<<k)
    j = 0
    cur = 1
    # inv: cur = 2^j
    res = []
    while j < k:
        if i & cur:
            res.append(v[j] == 1)
        else:
            res.append(v[j] == 0)
        j += 1
        cur *= 2
    return z3.And(res)

def build_formula(k, v=None):
    if v is None:
        v = build_variables(k)
    nb_blocks = 1<<k
    res = []
    for i in range(0, nb_blocks):
        block = get_block(k,i,v)
        res.append(z3.And(v[nb_blocks + 3*i] == 1, block))
        res.append(z3.And(v[nb_blocks + 3*i+1] == 1, block))
        res.append(z3.And(v[nb_blocks + 3*i+2] == 1, block))
    
    res = [z3.Or(res)]
    for var in v:
        res.append(var >= 0)
        res.append(var <= 1)

    return z3.And(res)

def build_variables(k):
    nb_blocks = 1<<k
    res = []
    for i in range(0, nb_blocks):
        res.append(z3.Int("a%d" % i))
    for i in range(0, nb_blocks):
        res.append(z3.Int("b%d" % i))
        res.append(z3.Int("c%d" % i))
        res.append(z3.Int("d%d" % i))
    return res


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Give a number")
        sys.exit(1)
    
    solver = z3.Solver()
    solver.add(build_formula(int(sys.argv[1])))
    print(solver.sexpr())
