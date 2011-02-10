import reader
from nfa2regexp import *
from nfa import *
import hachoir_regex as ha
foo = nfa(*reader.parse_head_file("examples/aplusbplus.head"))
conv = converter(foo)
conv.convert()
reg = [a for a in conv.edges[-1] if conv.edges[-1][a] == [13]][0]
