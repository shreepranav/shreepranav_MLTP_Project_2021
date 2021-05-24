from z3 import *

x1, x2, x3, x4, x5, x6, x7 = Reals('x1 x2 x3 x4 x5 x6 x7')
f1, f2, f3 = Reals('f1 f2 f3')
g1, g2 = Reals('g1 g2')
h1, h2 = Reals('h1 h2')

formula1 = And(x1==x2, x2==x3, x1!=x3)
formula2 = Or(x1==x2, x2==x3, x3==x4, x4!=x5, x5==x6, x6==x7)
formula3 = And(x1==x2, x4==x5, x5!=x1, x2==x3, f1!=f3, g1==g2, h1==h2)
formula4 = And(Or(x1==x2, x3!=x4), Or(x1==x4, x2==x4))
formula5 = Implies(And(x1==x2, x2==x3), x1==x3)
formula6 = Implies(Not(And(x1==x2, x2==x3)), Or(Not(x1==x2), Not(x2==x3)))
formula7 = And(Or(x1==x2, x2==x3, x3==x4), Or(x2==x1, x1==x4), Not(And(x3==x3, x2==x3)))
formula8 = And(x1==x2, x2==x3, x3==x4, x4==f1, f1==f2, f2==g1, g1==g2, g2==h1, h1==h2, h2!=x2)
formula9 = And(x1==x2, x1==x3, Or(x1!=x2, f1==f2), Or(x2!=x3, f2==f3), f1!=f3)
formula10 = And(x1==x2, Or(x2==x3, f2==f3), f1!=f3, Implies(x1==x3, f1==f3), Implies(x2==x3, f2==f3))