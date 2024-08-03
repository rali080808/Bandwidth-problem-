oo = 10000000

n = int(input())
m = int(input())

edges = []
for i in range(0, n+1):
    edges.append([])


for j in range(m):
    b = int(input())
    e = int(input())
    edges[b].append(e)
    edges[e].append(b)

#ALGORITHM I - finding a starting vertex

v = 1
for i in range(1, n+1):
    if len(edges[i]) < len(edges[v]):
        v = i


maxiLevel = -1
def bfsLevel(start):
    level = []
    for i in range(0, n+1):
        level.append(-1)
    q = [v]
    level[v] = 1
    maxiLevel = -1
    while len(q) != 0:
        curr = q[0]
        del(q[0])
        for next in edges[curr]:
            if level[next] == -1: 
                level[next] = level[curr] + 1
                if level[next] > maxiLevel:
                    maxiLevel = level[next]
                q.append(next)
    
    return level,maxiLevel

def findWidth(level):
    width = []
    for i in range(1, n+1):
        width.append(0)
    
    for l in level:
        width[l] = width[l] + 1

    maximalWidth = 0
    for w in width:
         if w > maximalWidth:
             maximalWidth = w
    
    return maximalWidth


levelV,maxiLevel = bfsLevel(v)
maxiLevelV = maxiLevel
u = -1
flag = 1
levelU = []
while flag == True:
    s = []
    for i in range(1, n+1):
        if levelV[i] == maxiLevelV:
            s.append(i)
                   
    flag = False
    next_s = [ (len(edges[next]), next) for next in s ]
    next_s.sort()
    minimalWidthS = oo 
    for _,next in next_s:
        levelS,maxiLevel = bfsLevel(next)
        if maxiLevel > maxiLevelV:
            maxiLevelV = maxiLevel
            v = next
            levelV = levelS
            flag = True
            break
        widthThisS = findWidth(levelS)
        if widthThisS < minimalWidthS:
            minimalWidthS = widthThisS
            u = next
            levelU = levelS
print('maxiLevelV=', maxiLevelV)
print("u=",u)
print("v=",v)
widthU = minimalWidthS
widthV = findWidth(levelV)
#The algorithm terminates with u and v the endpoints of the diameter

#ALGORITHM II - minimizing level width

alp = [-1,-1] * (n+1) #associated level pairs
for i in range(1, n+1):
    alp[i] = [ levelV[i], maxiLevelV - levelU[i] + 1 ]

levelN = [] * (n+1)

# step 1 - all verteces whose associated level pair is in the form (i,i) get removed from the graph
used = (n+1) * [False]
for w in range(1, n+1):
    if alp[w][0] == alp[w][1]:
        levelN[ alp[w][0] ].append(w)
        used[w] = True

#step 2 - Find the components and arrange them in descending order based on the number of vertices in each component
c = (n+1) * []
def dfs(start, component):
    used[start] = True
    c[component].append(start)
    for next in edges[start]:
        if used[next] == False:
            dfs(next)
component = 0
for i in range(1, n+1):
    if not used[i]:
        component += 1
        dfs(i, component)

next_component = [ (len(c[next]), c[next]) for next in range(0, n+1) ]
next_component.sort()

#step 3 - for each component do these a, b and c something

#sm A - n[i] is the width of levelN[i] for now(only w nodes)
n = (n+1) * [0]
for i in range(0, n+1):
    n[i] = len(levelN[i])

#sm B - compute the vectors h and l
h = [n[i] for i in range(n+1)]
l = [n[i] for i in range(n+1)]

for i, j in alp:
    h[i] += 1
    l[j] += 1 #?? maxiLevelV - j + 1

#sm C
l0 = 0
h0 = 0
for i in range(n+1):
    if l[i] - n[i] > 0:
        if l[i] > l0:
            l0 = l[i]
    
    if h[i] - n[i] > 0:
        if h[i] > h0:
            h0 = h[i]


for w in range(1, n+1):
    if alp[w][0] != alp[w][1]:
        if h0 < l0:
            levelN[ alp[w][0] ].append(w) 
        elif l0 < h0:
            levelN[ alp[w][1] ].append(w) #?? maxiLevelV - j + 1 
        else:
            if widthV < widthU:
                levelN[ alp[w][0] ].append(w) 
            else:
                levelN[ alp[w][1] ].append(w) #?? maxiLevelV - j + 1 

#ALGORITHM III -Numbering

#A
def swap(u,v):
    return v, u

if len(edges[u]) < len(edges[v]):
    u,v = swap(u,v)
    for i in range(1, n/2):
        levelN[i], levelN[maxiLevelV-i+1] = swap(levelN[i], levelN[maxiLevelV-i+1])

#B                
newI = (n+1) * [0]
oldI = (n+1) * [0]
num = 1

newI[v] = num
oldI[num] = v
num += 1
for k in range(1, maxiLevelV):
    for ni in range(1,n):
        if oldI[ni] == 0:
            continue #maybe break
        if oldI[ni] not in levelN[k]:
            continue
        next_edges = [(len(edges[i]), i) for i in edges[oldI[ni]]]
        for _, next in next_edges:
            newI[next] = num
            oldI[num] = next
            num += 1
    degree = oo
    
    for w in levelN[k]:
        if oldI[w] == 0:
            if 
   



