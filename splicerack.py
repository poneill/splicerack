#!/usr/bin/env python
import re, sys, os
from reader import *
from nfa import *
filename = "baaplus.head"

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    test = nfa(*parse_head_file(filename))
    f, ext = os.path.splitext(filename)
    test.graphviz(f)

