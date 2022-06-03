import sys

coms = [[2,3,4],[3,4],[4]]

successes = []

with open('successes_new.txt') as f:
    lines = f.readlines()
    for line in lines:
        successes.append([int(i) for i in line.split(' ')])

print(len(successes))

def w2str(w):
    return ''.join(str(i) for i in w)

def move_rt(w, n):
    for i in range(len(w)-1):
        if w[i] == n and w[i+1] in coms[n]:
            w[i] = w[i+1]
            w[i+1] = n

def replace_pattern(w, fr, to):
    for i in range(len(w)-len(fr)+1):
        if all(t[0]==t[1] for t in zip(fr,w[i:])):
            for j in range(len(to)):
                w[i+j] = to[j]

def canonicalize(w):
    after = w2str(w)
    while True:
        before = after
        move_rt(w,2)
        move_rt(w,1)
        move_rt(w,0)
        replace_pattern(w,[0,1,0],[1,0,1])
        replace_pattern(w,[1,2,1],[2,1,2])
        replace_pattern(w,[3,4,3],[4,3,4])
        replace_pattern(w,[2,3,2,3],[3,2,3,2])
        after = w2str(w)
        if before == after:
            break
    return w



uniques = set()
for a in successes:
    uniques.add(tuple(reversed(canonicalize(a))))
print("\n".join(str([x for x in reversed(u)]) for u in sorted(uniques)))

print(len(successes), len(uniques))
sys.exit(0)