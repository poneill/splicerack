from nfa import nfa

DEBUG = True
def debug(text):
    if DEBUG:
        print text

class converter(nfa):
    def __init__(self,automaton):
        self.edges = dict(automaton.edges)
        self.states = automaton.states[:]
        self.final_states = automaton.final_states[:]
        B = -1
        E = max(self.states) + 1
        self.add_edge(B,"",0)
        for f in self.final_states:
            self.add_edge(f,"",E)

    def convert(self):
        def parenthesize(s):
            return "(%s)" % s if "+" in s and not "(" == s[0] else s
 
        for qi in self.states:
            debug(qi)
            for qf in self.states:
                ts = self.find_transitions(qi,qf)
                if len (ts) > 1:
                    debug(ts)
                    label = "+".join([parenthesize(t) for t in ts])
                    debug(label)
                    self.remove_transitions(qi,qf)

    def find_transitions(self, qi,qf):
        """return a list of all transitions between qi and qf"""
        return [transition for transition in self.edges[qi] 
                if qf in self.edges[qi][transition]]

    def remove_transitions(self, qi, qf):
        for transition in self.edges[qi]:
            reachable_states = self.edges[qi][transition]
            if qf in reachable_states:
                self.edges[qi][transition].remove(qf)

foo = nfa(["baa,1;b,aa"],["baa"])
bar = converter(foo)
        