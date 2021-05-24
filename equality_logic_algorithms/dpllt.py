from z3 import *

pl_to_lit = []
pl_letters = []

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

# If literal has already been converted to a propositional letter, that propositional letter is returned
# Otherwise, a new propositional letter is created and is returned
def lit_to_pl(literal):
    root = literal.decl()
    if str(root) == '==':
        if set(literal.children()) not in pl_to_lit:
            pl_letters.append(Bool("p" + str(len(pl_letters) + 1)))
            pl_to_lit.append(set(literal.children()))
            return pl_letters[-1]
        else:
            i = pl_to_lit.index(set(literal.children()))
            return pl_letters[i]

# Converts an E formula into a PL formula
def convert_to_pl(formula):
    formula = implies_elim(formula)
    root = formula.decl()
    if str(root) == '==':
        [v, w] = formula.children()
        if str(v) == str(w):
            return True
        return lit_to_pl(formula)
    elif str(root) == 'Not':
        f = formula.children()[0]
        return Not(convert_to_pl(f))
    elif str(root) == 'Implies':
        f1 = formula.children()[0]
        f2 = formula.children()[1]
        return Implies(convert_to_pl(f1), convert_to_pl(f2))
    else:
        res = []
        for f in formula.children():
            res.append(convert_to_pl(f))
        if str(root) == 'And':
            return And(res)
        elif str(root) == 'Or':
            return Or(res)
        elif str(root) == 'Implies':
            return Implies(res)

#Function that implements the DPLL(T) algorithm for Equality Logic SAT
def dpllt(formula):
    global pl_letters
    global pl_to_lit
    pl_letters = []
    pl_to_lit = []  
    pl_formula = convert_to_pl(formula)
    s = Solver()
    s.add(pl_formula)
    result = s.check()
    while result == sat:        
        m = s.model()
        g1 = {}
        g2 = {}
        for i in range(len(pl_letters)):
            [v, w] = list(pl_to_lit[i])
            if m[pl_letters[i]] == True:
                addedge(g1, v, w)
            else:
                addedge(g2, v, w)
        cont_cycle = contradictory_cycle(g1, g2)
        if cont_cycle != None:
            new_clause = []
            for i in range(len(cont_cycle) - 1):
                j = pl_to_lit.index({cont_cycle[i], cont_cycle[i+1]})
                new_clause.append(Not(pl_letters[j]))
            new_clause.append(pl_letters[pl_to_lit.index({cont_cycle[0], cont_cycle[-1]})])
            s.add(Or(new_clause))
            result = s.check()
        else:
            pl_to_lit = []
            pl_letters = []
            return z3.sat
    pl_to_lit = []
    pl_letters = []
    return z3.unsat