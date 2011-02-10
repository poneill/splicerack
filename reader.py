#!/usr/bin/env python

import re

def parse_head_file(filename):
    with open(filename) as f:
        text = "".join(f.readlines())
    symmetric = eval(re.findall(r"symmetric ([0-1])",text)[0])
    reflexive = 1 if re.findall(r"type ([a-z-])",text)[0] == "head" else 0
    rules = re.findall(r"([a-z1]+,[a-z1]+;[a-z1]+,[a-z1]+)",text)
    axioms = re.findall(r"\[axioms\](.*)",text,re.DOTALL)[0].split()
    return (rules, axioms, reflexive, symmetric)
