#!/usr/bin/env python
import re, sys, os
from nfa import *
print sys.argv
filename = "ex84.hs"
if __name__ == '__main__':
    print __name__
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        text = "".join(f.readlines())
    symmetric = eval(re.findall(r"symmetric ([0-1])",text)[0])
    reflexive = 1 if re.findall(r"type ([a-z-])",text)[0] == "head" else 0
    rules = re.findall(r"([a-z1]+,[a-z1]+;[a-z1]+,[a-z1])+",text)
    axioms = re.findall(r"\[axioms\](.*)",text,re.DOTALL)[0].split()
    test = nfa(rules,axioms,reflexive,symmetric)
    f, ext = os.path.splitext(filename)
    test.graphviz(f)

