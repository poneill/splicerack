import reader
from nfa2regexp import *
from nfa import *
import hachoir_regex as ha
foo = nfa(*reader.parse_head_file("examples/baaplus.head"))
conv = converter(foo)
conv.convert()
reg = [a for a in conv.edges[-1] if conv.edges[conv.B][a] == [conv.E]][0]
print reg
