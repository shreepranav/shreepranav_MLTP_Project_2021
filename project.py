from z3 import *
import time
from timeit import default_timer as timer

class graph:

    def __init__(self, gdict = None):
        if gdict is None:
            gdict = {}
        self.gdict = gdict

    def getVertices(self):
        return list(self.gdict.keys())

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

pl_to_lit = []
pl_letters = []

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

#def pl_to_index(pl):
#    i = str(pl)[1:]
#    return eval(i)

# Converts an E formula into a PL formula
def convert_to_pl(formula):
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


def approach1(formula):
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
                return "SAT"
        else:
            return "SAT"
    return "UNSAT"

def approach2(formula):
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
            return "SAT"
    pl_to_lit = []
    pl_letters = []
    return "UNSAT"

def approach3(formula):          
    global pl_letters
    global pl_to_lit
    pl_letters = []
    pl_to_lit = []  
    pl_formula = convert_to_pl(formula)
    s = Solver()
    s.add(pl_formula)
    vertices = []
    for i in range(len(pl_letters)):
        [v, w] = list(pl_to_lit[i])
        if v not in vertices:
            vertices.append(v)
        if w not in vertices:
            vertices.append(w)
    for i in vertices:
        for j in vertices:
            for k in vertices:
                if (i == j or j == k or k == i):
                    continue
                if({i, j} not in pl_to_lit):
                    pl_to_lit.append({i, j})
                    pl_letters.append(Bool("p" + str(len(pl_letters) + 1)))
                    a = len(pl_letters) - 1
                else:
                    a = pl_to_lit.index({i, j})
                if({j, k} not in pl_to_lit):
                    pl_to_lit.append({j, k})
                    pl_letters.append(Bool("p" + str(len(pl_letters) + 1)))
                    b = len(pl_letters) - 1
                else:
                    b = pl_to_lit.index({j, k})
                if({i, k} not in pl_to_lit):
                    pl_to_lit.append({i, k})
                    pl_letters.append(Bool("p" + str(len(pl_letters) + 1)))
                    c = len(pl_letters) - 1
                else:
                    c = pl_to_lit.index({i, k})
                s.add(Or(Not(pl_letters[a]), Not(pl_letters[b]), pl_letters[c]))
    result = s.check()
    if result == sat:
        return "SAT"
    else:
        return "UNSAT"
                
                

# Declare uninterpreted constants and input the formula here
x1, x2, x3, x4, x5, x6, x7, f1, f2, f3, g1, g2, h1, h2 = Ints('x1 x2 x3 x4 x5 x6 x7 f1 f2 f3 g1 g2 h1 h2')   
formula = And(x1 == x2, Implies(x1 == x2, x2 == x3), Not(x1 == x3))



g1 = {}
g2 = {}


start = timer()
res = approach1(formula)
end = timer()
print("Approach 1: ", res, ",", end - start)

start = timer()
res = approach2(formula)
end = timer()
print("Approach 2: ", res, ",", end - start)

start = timer()
res = approach3(formula)
end = timer()
print("Approach 3: ", res, ",", end - start)