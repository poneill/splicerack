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

    def convert(self, automaton):
            for qi in self.states:
                debug(qi)
                for qf in self.states:
                    ts = self.find_transitions(qi,qf)
                    if len(ts) > 1
                    label = "+".join(["(%s)" % t for t in ts])
                    self.remove_transitions(qi,qf)

    def find_transitions(self, qi,qf):
        """return a list of all transitions between qi and qf"""
        return [transition for transition in self.edges[qi] 
                if qf in self.edges[qi][transition]]

    def remove_transitions(self, qi, qf):
        pass
        
