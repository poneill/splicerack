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
    
    def parenthesize(self, s):
        return "(%s)" % s if "+" in s and not "(" == s[0] else s

    def convert(self): 
        for state in self.states:
            incoming_edges = self.incoming_edges(state)[:]#copies, since we'll
            loops = self.loops(state)[:]                  #be deleting as we go
            outgoing_edges = self.outgoing_edges(state)[:]
            for (in_qi, in_label, in_qf) in incoming_edges: #(qi,a,qf)
                for (loop_qi, loop_label, loop_qf) in loops: # simile
                    for (out_qi, out_label, out_qf) in outgoing_edges:#simile
                        label = (in_label + self.parenthesize(loop_label)
                                 + "*" + out_label)
                        self.add_edge(in_qi,label,out_qf)
                        self.remove_edge(in_qi, in_label, in_qf)
                        self.remove_edge(out_qi, out_label, out_qf)

    def incoming_edges(self, q):
        debug(q)
        return [(qi,a,q) for qi in self.edges for a in self.edges[qi]
                if q in self.edges[qi][q]]
    
    def loops(self,q):
        return [(q,a,q) for a in self.edges[q] if q in self.edges[q][a]]

    def outgoing_edges(self,q):
        return [(q,a,qf) for a in self.edges[q] for qf in self.edges[q][a]]

    def remove_edge(self, qi, a, qf):
        if a in self.edges[qi] and qf in self.edges[qi][a]:
            self.edges[qi][a].remove(qf)

    def condense_multiple_edges(self, qi=None,qf=None):
        def condense(qi,qf):
            ts = self.find_edges(qi,qf)
            if len (ts) > 1:
                debug(ts)
                label = "+".join([self.parenthesize(t) for t in ts])
                debug(label)
                self.remove_edges(qi,qf)
                self.add_edge(qi,label,qf)
        if qi and qf:
            condense(qi, qf)
        else:
            for qi in self.states:
                for qf in self.states:
                    condense(qi, qf)


    def find_edges(self, qi,qf):
        """return a list of all edges between qi and qf"""
        return [edge for edge in self.edges[qi] 
                if qf in self.edges[qi][edge]]

    def remove_edges(self, qi, qf):
        """remove all edges from qi to qf"""
        for edge in self.edges[qi]:
            reachable_states = self.edges[qi][edge]
            if qf in reachable_states:
                self.edges[qi][edge].remove(qf)
    
foo = nfa(["baa,1;b,aa"],["baa"])
bar = converter(foo)
