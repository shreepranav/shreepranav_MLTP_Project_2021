from z3 import *

# Finds a path between start and end in graph
# Returns None if there is no path    
def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in graph.keys():
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    return None

# Returns a list of all edges in graph (edges are stored as sets of vertices)
def findedges(graph):
    edges = []
    for v in graph.keys():
        for w in graph[v]:
            if {v, w} not in edges:
                edges.append({v, w})
    return edges

# Adds an edge between v and w in graph
def addedge(graph, v, w):
    if v in graph.keys():
        graph[v].append(w)
    else:
        graph[v] = [w]
    if w in graph.keys():
        graph[w].append(v)
    else:
        graph[w] = [v]

# Returns a contradictory cycle (edges in g1 are taken to be dashed and edges in g2 are solid)
# Returns None if there is no contradictory cycle
def contradictory_cycle(g1, g2):
    for e in findedges(g2):
        if len(list(e)) == 1:
            return list(e)
        v, w = list(e)
        if (find_path(g1, v, w) != None):
            return find_path(g1, v, w)
    return None

# Merges the two conjunctions f1 and f2 into a single conjunction and returns it
def and_merge(f1, f2):
    result = set([])
    if (str(f1.decl()) != 'And'):
        result.add(f1)
    else:
        result = result.union(set(f1.children()))
    if (str(f2.decl()) != 'And'):
        result.add(f2)
    else:
        result = result.union(set(f2.children()))
    return And(result)

# Eliminates all 'Implies' predicates from the formula in favour of 'Not' and 'Or'
def implies_elim(formula):
    root = str(formula.decl())
    if (root == '=='):
        return formula
    elif (root == 'Distinct'):
        return Not(formula.children()[0] == formula.children()[1])
    elif (root == 'Implies'):
        [f1, f2] = formula.children()
        f1 = implies_elim(f1)
        f2 = implies_elim(f2)
        return Or(Not(f1), f2)
    elif (root == 'Not'):
        return Not(implies_elim(formula.children()[0]))
    else:
        res = []
        for i in range(len(formula.children())):
            res.append(implies_elim(formula.children()[i]))
        if (root == 'And'):
            return And(res)
        if (root == 'Or'):
            return Or(res)       

# Converts formula into negation normal form
def negation_normal_form(formula):
    formula = implies_elim(formula)
    root = str(formula.decl())
    if (root == '=='):
        return formula
    elif (root == 'And' or root == 'Or'):
        res = []
        for i in range(len(formula.children())):
            res.append(negation_normal_form(formula.children()[i]))
        if (root == 'And'):
            return And(res)
        elif (root == 'Or'):
            return Or(res)
    elif (root == 'Not'):
        f = formula.children()[0]
        r = str(f.decl())
        if (r == 'Not'):
            return negation_normal_form(f.children()[0])
        elif (r == '=='):
            return formula
        else:
            list = []
            for i in range(len(f.children())):
                child = (negation_normal_form(Not(f.children()[i])))
                list.append(child)
            if (r == 'And'):
                return Or(list)
            elif (r == 'Or'):
                return And(list)        
    return formula

# Converts formula into DNF
def convert_to_dnf(formula):
    formula = negation_normal_form(formula)
    root = str(formula.decl())
    result = set([])
    if (root == '==' or root == 'Not'):
        return {formula}
    elif (root == 'Or'):
        for f in formula.children():
            result = result.union(convert_to_dnf(f))
    elif (root == 'And'):
        f1 = formula.children()[0]
        f2 = formula.children()[1:]
        l1 = convert_to_dnf(f1)
        if (len(f2) > 1):
            l2 = convert_to_dnf(And(f2))
        else:
            l2 = convert_to_dnf(f2[0])
        for i in l1:
            for j in l2:
                result.add(and_merge(i, j))
    return result

#Function that implements DNF + Equality Graph algorithm for Equality Logic SAT
def dnf_eg(formula):
    formula = negation_normal_form(formula)
    dnf = convert_to_dnf(formula)    
    for conjunction in dnf:
        g1 = {}
        g2 = {}
        root = conjunction.decl()
        if str(root) == "And":
            for literal in conjunction.children():
                if str(literal.decl()) == '==':
                    addedge(g1, literal.children()[0], literal.children()[1])
                elif str(literal.decl()) == 'Not':
                    l = literal.children()[0]
                    addedge(g2, l.children()[0], l.children()[1])
            if contradictory_cycle(g1, g2) == None:
                return z3.sat
        else:
            return z3.sat
    return z3.unsat 