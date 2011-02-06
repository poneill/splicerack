import subprocess, shlex

class nfa(object):
    def __init__(self, rules, axioms,reflexive=False,symmetric=False):
        self.rules = []
        self.axioms = axioms
        self.states = [0]
        self.final_states = []
        self.edges = {}
        self.bridges = []
        self.symmetric = symmetric
        self.reflexive = reflexive
        self.accepting_paths = {}
        self.construct_rules(rules)
        self.construct_axioms()
        self.construct_bridges()
        snapshot = {}
        while (snapshot != self.edges):
            snapshot = dict(self.edges)
            self.construct_null_transitions()

    def add_to_rules(self,rule):
        if not rule in self.rules:
            self.rules.append(rule)
            
    def add_edge(self,qi,a,qf):
        if not qi in self.edges:
            self.edges[qi] = {}
        if not a in self.edges[qi]:
            self.edges[qi][a] = []
        if not qf in self.edges[qi][a]:
            self.edges[qi][a].append(qf)

    def construct_rules(self,rules):
        formatting = lambda x: ' ' if x == ',' or x == ';' else x 
        handle_empty_string = lambda x: x if x != "1" else ""        
        for rule in rules:
            r1,r2,r3,r4 = map(handle_empty_string,
                              "".join(map(formatting,rule)).split())
            self.rules.append((r1,r2,r3,r4))
            if self.symmetric:
                self.add_to_rules((r3,r4,r1,r2))
            if self.reflexive:
                self.add_to_rules((r1,r2,r1,r2))
                self.add_to_rules((r3,r4,r4,r4))
                
    def construct_axioms(self):
        for axiom in self.axioms:
            qi = 0
            qf = max(self.states) + 1
            for a in axiom:
                self.add_edge(qi,a,qf)
                self.states.append(qf)
                qi = qf
                qf += 1
            self.final_states.append(qi)
    
    def construct_bridges(self):
        if self.rules and not self.bridges:
            for rule in self.rules:
                r1,r2,r3,r4 = rule
                q_init = max(self.states) + 1
                self.states.append(q_init)
                qi = q_init
                qf = qi
                for a in r1+r4:
                    qi = qf
                    qf += 1
                    self.add_edge(qi,a,qf)
                    self.states.append(qf)
                self.bridges.append([q_init,qf,rule])

    def construct_null_transitions(self):
        for q in self.states:
            for qi, qt, r in self.bridges:
                r1, r2, r3, r4 = r
                if (not self.initial_in_bridge(q) and 
                        self.at_state_before_reading(q,r1+r2)): 
                    print "adding edge (%s %s %s)" % (q, "", qi)
                    self.add_edge(q,"",qi)
            for qi, qt, r in self.bridges:
                r1, r2, r3, r4 = r
                print 
                if (not self.terminal_in_bridge(q) and
                        self.at_state_after_reading(q,r3+r4)):
                    #print "adding edge (%s %s %s) term: %s at_state_after: %s,word: %s" % (qt, "", q,self.terminal_in_bridge(q),
                    #                                                              self.at_state_after_reading(q,r3+r4),r3+r4)
                    #DEBUG
                    self.add_edge(qt,"",q)

    def initial_in_bridge(self,q):
        return any([q==bi for bi, bt, rule in self.bridges])
    
    def terminal_in_bridge(self,q):
        return any([q==bt for bi, bt, rule in self.bridges])

    def exists_accepting_path_from(self,q):
        def eapf(q):
            snapshot = dict(self.accepting_paths) 
            print "now checking %s" % q
            print "accepting paths: %s" % snapshot
            if q in snapshot:
                print "found %s in accepting paths" % q
                if snapshot[q] == 2:
                    print "already searching for %s" % q
                    return False
                else:
                    return snapshot[q]
            else:
                snapshot[q] = 2 #2 means "maybe"
            if q in self.final_states:
                print "found %s in final states" % q
                snapshot[q] = True
                result = True
            elif not q in self.edges:
                print "no edges from %s" % q
                snapshot[q] = False
                result = False
            else:
                for transition in self.edges[q].values():
                    print "transition: %s" % transition
                    for state in transition:
                        print "state %s" % state
                result = any([eapf(state) 
                            for transition in self.edges[q].values()
                            for state in transition])
                snapshot[q] = result
            for q in snapshot:
                if snapshot[q] == True:
                    self.accepting_paths[q] = True
            return result
        result = eapf(q)
        return result

    def transitions(self,q,xs,trans_dict={}):
        td = dict(trans_dict) #otherwise you accidentally a closure
        #print "calling transitions with %s, %s, %s" %(q,xs,td)
        if (q,xs) in td:
            if td[(q,xs)]:
                return td[(q,xs)]
            else:
                return []
        else:
            td[(q,xs)] = None #"start the file" for q,xs"
        if not q in self.edges:
            if not xs:
                return [q]
            else:
                return []
        elif not xs:
            return reduce(lambda x,y:x+y,[self.transitions(r,xs,td) 
                                                 for a in self.edges[q] 
                                                 for r in self.edges[q][a] 
                                                 if a == "" and r != q],[q])
        else:
            ys = xs
            x,xs = xs[0], xs[1:]
            trans = reduce(lambda x,y:x+y,[self.transitions(r,xs,td) 
                                                 for a in self.edges[q] 
                                                 for r in self.edges[q][a] 
                                                 if a == x],[])
            null_trans = reduce(lambda x,y:x+y,[self.transitions(r,ys,td) 
                                                 for a in self.edges[q] 
                                                 for r in self.edges[q][a] 
                                                 if a == "" and r != q],[])
            td[(q,xs)] = trans + null_trans
            return td[(q,xs)]

    def at_state_before_reading(self,q,xs):
        print "determining if at %s before reading %s" % (q,xs)
        at_state = self.exists_accepting_path_from(q)
        transitions = self.transitions(q,xs)
        return at_state and any([self.exists_accepting_path_from(t) 
                                 for t in transitions])
    
    def at_state_after_reading(self,q,xs):
        print "determining if at %s after reading %s" % (q,xs)
        transitions = [i for state in self.states 
                       for i in self.transitions(state,xs)]
        return q in transitions and self.exists_accepting_path_from(q)

    def read(self, word):
        return any([state in self.final_states
                    for state in self.transitions(0,word)])

    def graphviz(self,filename):
        template = ("digraph %s " % filename) + "{\n%s\n%s\n}"
        def bridge_text(q):
            intervals = [range(qi,qt+1) for qi,qt,rule in self.bridges]
            in_bridge = any([q in interval for interval in intervals])
            rule_number = [i + 1 for i,interval in enumerate(intervals) 
                           if q in interval]
            inits = [interval[0] for interval in intervals]
            terms = [interval[-1] for interval in intervals] 
            init_text = ',label="init %s"'%q if q in inits else ""
            term_text = ',label="term %s"'%q if q in terms else ""
            rule_text = (",label=r%s %s" % (rule_number[0],q)
                         if rule_number and not (init_text or term_text) 
                         else "")
            if in_bridge:
                return "[shape = box" + init_text + term_text + rule_text + "]"
            else:
                return ""
        state_text = "\n".join([str(q) + bridge_text(q) for q in self.states])
        edges_text = "\n".join(['%s -> %s [label="%s"];' % (qi,qf,a if a else "1") 
                for qi in self.edges 
                for a in self.edges[qi] 
                for qf in self.edges[qi][a]])
        with open("%s.dot" % filename,'w') as f:
            f.write(template % (state_text,edges_text))
        command = shlex.split(("dot %s.dot -Tps" % filename))
        task = subprocess.Popen(command, stdout=subprocess.PIPE)
        with open("%s.ps" % filename,'w') as g:
            g.write("".join(task.stdout.readlines()))

