import time
import sys
from timeit import default_timer as timer

# For D_4^(3)
# A = [[2,-1,0,0,0],[-1,2,-1,0,0],[0,-3,2,0,0],[0,0,0,0,0],[0,0,0,0,0]]

# For G_2^(1)
# A = [[2,-1,0,0,0],[-1,2,-3,0,0],[0,-1,2,0,0],[0,0,0,0,0],[0,0,0,0,0]]

# For E_2^(6)
A = [[2,-1,0,0,0],[-1,2,-1,0,0],[0,-1,2,-1,0],[0,0,-2,2,-1],[0,0,0,-1,2]]

# For F_4^(1)
#A = [[2,-1,0,0,0],[-1,2,-1,0,0],[0,-1,2,-2,0],[0,0,-1,2,-1],[0,0,0,-1,2]]

w0 = [4, 3, 2, 3, 1, 2, 3, 4, 3, 2, 3, 1, 2, 3, 4, 3, 2, 3, 1, 2, 3, 1, 2, 0]
required = [[1,0,1,2,1,1],[0,1,3,3,1,2]]

f4len6 = [[1, 2, 1, 0, 1, 2], [3, 2, 1, 0, 1, 2], [1, 2, 1, 0, 1, 3], [3, 2, 1, 0, 1, 3], [1, 2, 1, 0, 1, 4], [3, 2, 1, 0, 1, 4], [0, 2, 1, 0, 2, 1], [3, 2, 1, 0, 2, 1], [0, 2, 1, 0, 2, 3], [3, 2, 1, 0, 2, 3], [0, 2, 1, 0, 2, 4], [3, 2, 1, 0, 2, 4], [0, 2, 1, 0, 3, 2], [1, 2, 1, 0, 3, 2], [3, 2, 1, 0, 3, 2], [0, 2, 1, 0, 3, 4], [1, 2, 1, 0, 3, 4], [3, 2, 1, 0, 3, 4], [0, 2, 1, 0, 4, 3], [1, 2, 1, 0, 4, 3], [3, 2, 1, 0, 4, 3], [0, 3, 2, 1, 0, 2], [1, 0, 2, 1, 0, 2], [0, 4, 3, 1, 0, 2], [4, 3, 2, 1, 0, 2], [2, 3, 2, 1, 0, 2], [0, 3, 2, 1, 0, 3], [1, 0, 2, 1, 0, 3], [0, 1, 2, 1, 0, 3], [4, 3, 2, 1, 0, 3], [2, 3, 2, 1, 0, 3], [1, 3, 2, 1, 0, 3], [0, 3, 2, 1, 0, 4], [1, 0, 2, 1, 0, 4], [0, 4, 3, 1, 0, 4], [0, 1, 2, 1, 0, 4], [4, 3, 2, 1, 0, 4], [2, 3, 2, 1, 0, 4], [1, 3, 2, 1, 0, 4], [0, 4, 3, 1, 2, 1], [1, 0, 3, 1, 2, 1], [0, 3, 2, 1, 2, 3], [1, 0, 2, 1, 2, 3], [0, 4, 3, 1, 2, 3], [1, 0, 3, 1, 2, 3], [4, 3, 2, 1, 2, 3], [2, 3, 2, 1, 2, 3], [0, 3, 2, 1, 2, 4], [1, 0, 2, 1, 2, 4], [0, 4, 3, 1, 2, 4], [1, 0, 3, 1, 2, 4], [4, 3, 2, 1, 2, 4], [2, 3, 2, 1, 2, 4], [0, 3, 2, 1, 3, 2], [1, 0, 2, 1, 3, 2], [0, 1, 2, 1, 3, 2], [4, 3, 2, 1, 3, 2], [2, 3, 2, 1, 3, 2], [1, 3, 2, 1, 3, 2], [0, 3, 2, 1, 3, 4], [1, 0, 2, 1, 3, 4], [0, 1, 2, 1, 3, 4], [4, 3, 2, 1, 3, 4], [2, 3, 2, 1, 3, 4], [1, 3, 2, 1, 3, 4], [0, 3, 2, 1, 4, 3], [1, 0, 2, 1, 4, 3], [1, 0, 3, 1, 4, 3], [0, 1, 2, 1, 4, 3], [4, 3, 2, 1, 4, 3], [2, 3, 2, 1, 4, 3], [1, 3, 2, 1, 4, 3], [0, 4, 3, 2, 1, 0], [1, 0, 3, 2, 1, 0], [0, 1, 0, 2, 1, 0], [0, 1, 3, 2, 1, 0], [2, 1, 3, 2, 1, 0], [0, 2, 3, 2, 1, 0], [1, 2, 3, 2, 1, 0], [3, 2, 3, 2, 1, 0], [1, 4, 3, 2, 1, 0], [2, 4, 3, 2, 1, 0], [3, 4, 3, 2, 1, 0], [0, 4, 3, 2, 1, 3], [1, 0, 3, 2, 1, 3], [0, 1, 0, 2, 1, 3], [2, 1, 0, 2, 1, 3], [0, 1, 3, 2, 1, 3], [2, 1, 3, 2, 1, 3], [0, 2, 3, 2, 1, 3], [1, 2, 3, 2, 1, 3], [1, 4, 3, 2, 1, 3], [2, 4, 3, 2, 1, 3], [3, 4, 3, 2, 1, 3], [0, 4, 3, 2, 1, 4], [1, 0, 3, 2, 1, 4], [0, 1, 0, 2, 1, 4], [2, 1, 0, 2, 1, 4], [0, 1, 3, 2, 1, 4], [2, 1, 3, 2, 1, 4], [0, 2, 3, 2, 1, 4], [1, 2, 3, 2, 1, 4], [3, 2, 3, 2, 1, 4], [1, 4, 3, 2, 1, 4], [2, 4, 3, 2, 1, 4], [0, 4, 3, 2, 3, 2], [1, 0, 3, 2, 3, 2], [0, 1, 0, 2, 3, 2], [2, 1, 0, 2, 3, 2], [0, 1, 3, 2, 3, 2], [2, 1, 3, 2, 3, 2], [1, 4, 3, 2, 3, 2], [3, 4, 3, 2, 3, 2], [0, 4, 3, 2, 3, 4], [1, 0, 3, 2, 3, 4], [0, 1, 0, 2, 3, 4], [2, 1, 0, 2, 3, 4], [0, 1, 3, 2, 3, 4], [2, 1, 3, 2, 3, 4], [0, 2, 3, 2, 3, 4], [1, 2, 3, 2, 3, 4], [1, 4, 3, 2, 3, 4], [2, 4, 3, 2, 3, 4], [3, 4, 3, 2, 3, 4], [0, 4, 3, 2, 4, 3], [1, 0, 3, 2, 4, 3], [0, 1, 0, 2, 4, 3], [2, 1, 0, 2, 4, 3], [0, 1, 3, 2, 4, 3], [2, 1, 3, 2, 4, 3], [0, 2, 3, 2, 4, 3], [1, 2, 3, 2, 4, 3], [3, 2, 3, 2, 4, 3], [1, 4, 3, 2, 4, 3], [2, 4, 3, 2, 4, 3], [0, 3, 2, 3, 2, 1], [1, 0, 2, 3, 2, 1], [0, 1, 0, 3, 2, 1], [2, 1, 0, 3, 2, 1], [0, 2, 1, 3, 2, 1], [1, 2, 1, 3, 2, 1], [3, 2, 1, 3, 2, 1], [0, 1, 2, 3, 2, 1], [0, 1, 4, 3, 2, 1], [0, 2, 4, 3, 2, 1], [0, 3, 4, 3, 2, 1], [2, 1, 4, 3, 2, 1], [2, 3, 4, 3, 2, 1], [1, 0, 4, 3, 2, 1], [1, 2, 4, 3, 2, 1], [1, 3, 4, 3, 2, 1], [3, 2, 4, 3, 2, 1], [1, 0, 2, 3, 2, 3], [0, 1, 0, 3, 2, 3], [2, 1, 0, 3, 2, 3], [0, 2, 1, 3, 2, 3], [1, 2, 1, 3, 2, 3], [3, 2, 1, 3, 2, 3], [0, 1, 2, 3, 2, 3], [0, 1, 4, 3, 2, 3], [0, 2, 4, 3, 2, 3], [0, 3, 4, 3, 2, 3], [2, 1, 4, 3, 2, 3], [2, 3, 4, 3, 2, 3], [1, 0, 4, 3, 2, 3], [1, 2, 4, 3, 2, 3], [1, 3, 4, 3, 2, 3], [3, 2, 4, 3, 2, 3], [0, 3, 2, 3, 2, 4], [1, 0, 2, 3, 2, 4], [0, 1, 0, 3, 2, 4], [2, 1, 0, 3, 2, 4], [0, 2, 1, 3, 2, 4], [1, 2, 1, 3, 2, 4], [3, 2, 1, 3, 2, 4], [0, 1, 2, 3, 2, 4], [0, 1, 4, 3, 2, 4], [0, 2, 4, 3, 2, 4], [2, 1, 4, 3, 2, 4], [1, 0, 4, 3, 2, 4], [1, 2, 4, 3, 2, 4], [3, 2, 4, 3, 2, 4], [0, 3, 2, 3, 4, 3], [1, 0, 2, 3, 4, 3], [0, 1, 0, 3, 4, 3], [2, 1, 0, 3, 4, 3], [0, 2, 1, 3, 4, 3], [1, 2, 1, 3, 4, 3], [3, 2, 1, 3, 4, 3], [0, 1, 2, 3, 4, 3], [0, 3, 2, 4, 3, 2], [1, 0, 2, 4, 3, 2], [1, 0, 3, 4, 3, 2], [0, 1, 0, 4, 3, 2], [2, 1, 0, 4, 3, 2], [0, 2, 1, 4, 3, 2], [1, 2, 1, 4, 3, 2], [3, 2, 1, 4, 3, 2], [0, 1, 2, 4, 3, 2], [4, 3, 2, 4, 3, 2], [2, 3, 2, 4, 3, 2], [1, 3, 2, 4, 3, 2], [0, 1, 3, 4, 3, 2], [2, 1, 3, 4, 3, 2], [0, 2, 3, 4, 3, 2], [1, 2, 3, 4, 3, 2], [3, 2, 3, 4, 3, 2]]
f4len12 = []
for i in f4len6:
    for j in f4len6:
        if j[0]>i[5] or j[0]==i[5]-1:
            f4len12.append(i+j)
        
print(len(f4len12))

def negs(w):
    output = []
    l = len(w)
    root = [0,0,0,0,0]
    root[w[l-1]]-=1
    output.append(root)
    for i in range(1,l):
        root = [0,0,0,0,0]
        root[w[l-1-i]]+=1
        for j in range(l-1-i, l):
            index = w[j]
            root[index] -= dot_product(root, index)
        if root[0]>0 or root[1]>0 or root[2]>0 or root[3]>0 or root[4]>0:
            return None
        output.append(root)
    
    return output

def dot_product(vect, index):
    return sum(vect[i]*A[i][index] for i in range(5))

def weyl(w, root):
    output = root
    l=len(w)
    for i in range(0,l):
        index = w[l-i-1]
        output[index] -= dot_product(output, index)
    return(output)

# Gives <w(\alpha_r), \Lambda_k>
def check(w, r, k):
    output = [0,0,0,0,0]
    
    l=len(w)
    
#    v=[]
#    for i in range(0,l):
#        v.append(w[i])
#    v.append(r)
#    for i in range(0,l):
#        v.append(w[l-i-1])
    v = w+[r]+w[::-1]
#    print(v)
    l = len(v)
    
    for i in range(0,l):
        index = v[l-i-1]
        delta = 0
        if index == k:
            delta+=1
        output[index] -= delta + dot_product(output, index)
    return output

def final(w, k):
    n = negs(w)
    if n is None:
        return None
    w.reverse()
    l=len(w)
    
    output = []
    v=[]
    for i in range(0,l):
        #print(i,v,w[i],check(v,w[i],0))        
        ans = sum(check(v,w[i],k))
        denom = sum(n[i])
        result = int(ans/denom)
        if result> 4 or result < 0:
            return None
        output.append(result)
        v.append(w[i])
    w.reverse()
    return output

def print_required():
    print(required[0])
    print(required[1])
    print()
    return

def demazure(w, k):
    w.reverse()
    output = [[0,0,0,0,0]]
    for i in w:
        #print i
        to_add = []
        to_del = []
        for root in output:
            m = dot_product(root, i)
            if i == k:
                m += 1
            #print (root, i, k, m)
            if m>=1:
                new_root = root.copy()
                for j in range(0,m):
                    new_root[i] -= 1
                    new_new_root = new_root.copy()
                    to_add.append(new_new_root)
                    
                    #print
            if m < 0:
                new_root = root.copy()
                
                for j in range(0,-m):  
                    #print new_root
                    new_new_root = new_root.copy()
                    to_del.append(new_new_root)
                    #print to_del
                    new_root[i] += 1
                      
                    #print to_del
                    
            #print ("add",to_add)
            #print ("delete",to_del)
            #print 
        #print ("output", output)
        #print ("toadd",to_add)
        #print ("todel",to_del)
        #print
        output.extend(to_add)
        for bad in to_del:
            output.remove(bad)
    #print
    #print
    w.reverse()              
    return output
        

#print_required()

#print(negs(w0))
#pos = []
#for neg in negs(w0):
#    pos.append(weyl(w0,neg))
#print(pos)

print

#for i in range(0,5):
#    print(final(w0,i))

print


f4len12 = []
with open('f4len12WithOut101n212.txt') as f:
    lines = f.readlines()
    for line in lines:
        f4len12.append([int(i) for i in line.split(' ')])

#f4len24 = []
#with open('f4len24new.txt') as f:
#    lines = f.readlines()
#    for line in lines:
#        f4len24.append([int(i) for i in line.split(' ')])
            



#print(f4len12, len(f4len12))



#for i in range(6,12):
#    to_remove = []
#    for w in f4len12:
#        M = negs(w)
#        if M[i][0]>0 or M[i][1]>0 or M[i][2]>0 or M[i][3]>0 or M[i][4]>0:
#            to_remove.append(w)
#    for w in to_remove:
#        f4len12.remove(w)
#    print(len(f4len12))

#with open('f4len12new.txt','w') as writer:
#    for w in f4len12:
#        writer.write(' '.join(str(a) for a in w) + '\n')

#sys.exit(0)

start = timer()
f4len24 = []
for i in f4len12:
    for j in f4len12:
        if j[0]>i[11] or j[0]==i[11]-1:
            f4len24.append(i+j)
end = timer()



#with open('f4len24new.txt','w') as writer:
#    for w in f4len24:
#        writer.write(' '.join(str(a) for a in w) + '\n')

REQUIRED = [(9,8,7,0,0),(4,6,9,2,3),(4,12,6,2,0),(9,14,1,0,0)]

def count(a):
    output = [0,0,0,0,0]
    for i in a:
        if 0<=i and i<=4:
            output[i]+=1
    return tuple(output)

def test(w):
#    print(w)
    N = negs(w)
    if N == None:
        return False
    
    M = [final(w,i) for i in range(5)]
    
#    print(M)
    if sum(x is not None for x in M) < 4:
        return False
    errors = 0
    for k in range(5):
        if k==4 and errors == 0:
            return True
        if M[k] is None or count(M[k]) not in REQUIRED:
            errors+=1
        if errors>1:
            return False
    return True

w0 = [4, 3, 2, 1, 3, 2, 3, 4, 3, 2, 1, 3, 2, 3, 4, 3, 2, 1, 3, 2, 3, 2, 1, 0]

print(len(f4len24), end-start)
print(test([4, 3, 2, 3, 1, 2, 3, 4, 3, 2, 3, 1, 2, 3, 4, 3, 2, 3, 1, 2, 3, 0, 1, 0]))


sys.exit(0)




successes = []
start = timer()
for k in range(4000000,len(f4len24)):
    if test(f4len24[k]) == True:
        successes.append(f4len24[k])
#        print("="*80)
    if k % 1000 == 0:
        print(k, "iterations are done")
end = timer()

print(len(successes), end-start)
print(successes)

with open('successes_new.txt','a') as writer:
#    writer.write('blah blah\n')
    for w in successes:
        if 0 in w:
            writer.write(' '.join(str(a) for a in w) + '\n')

sys.exit(0)





    


#print(final(w0,0))
#print(final(w0,1))
#print(final(w0,2))

#print(len(f4len6))



print
#print(demazure(w0,1))
#print(len(demazure(w0,0)))
