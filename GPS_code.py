oo = 10000000

n = int(input())
m = int(input())

edges = [[] for _ in range(0, n+1)]
 


for j in range(m):
    b = int(input())
    e = int(input())
    edges[b].append(e)
    edges[e].append(b)

newI = [0] * (n+1)
oldI = [0] * (n+1)
bandwidth = 0
num = 1
while True: # big
    
    flag = True
    for w in range(1, n+1):
        if newI[w] == 0:
            flag = False
            break
    
    if flag == True: 
        break
    #ALGORITHM I - finding a starting vertex

    v = -1
    for i in range(1, n+1):
        if newI[i] == 0:
            v = i
            break

    for i in range(1, n+1):
        if len(edges[i]) < len(edges[v]) and newI[i]==0:
            v = i

    maxiLevel = -1
    def bfsLevel(start):
        level = [ (-1) for _ in range(0, n+1)]
        q = [start]
        level[start] = 1
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
        width = [ (0) for _ in range(0, n+1)]
         
        
        for l in level:
            if ( l != -1 ):
                width[l] = width[l] + 1

        maximalWidth = 0
        for w in width:
            if w > maximalWidth:
                maximalWidth = w
        
        return maximalWidth

    verticesInThisComponent = []
    levelStructureV,maxiLevel = bfsLevel(v)
  
    for w in range(1, n+1):
        if levelStructureV[w] != -1:
            verticesInThisComponent.append(w)
    print("vertices in this component = ", verticesInThisComponent)         

    maxiLevelV = maxiLevel
    u = -1
    flag = 1
    levelStructureU = []
    while flag == True:
        s = []
        for i in range(1, n+1):
            if i in verticesInThisComponent:
                if levelStructureV[i] == maxiLevelV:
                    s.append(i)
        
                
        flag = False
        next_s = [ (len(edges[next]), next) for next in s ]
        next_s.sort()
        minimalWidthS = oo 
        for _,next in next_s:
            levelStructureS,maxiLevel = bfsLevel(next)
            if maxiLevel > maxiLevelV:
                maxiLevelV = maxiLevel
                v = next
                levelStructureV = levelStructureS.copy()
                flag = True
                break
            widthThisS = findWidth(levelStructureS)
            if widthThisS < minimalWidthS:
                minimalWidthS = widthThisS
                widthU = minimalWidthS
                u = next

    print('maxiLevelV=', maxiLevelV)
    print("v=",v)
    print("u=",u)
    widthU = minimalWidthS # izlishno, zashtoto go slozhih na line 112
    widthV = findWidth(levelStructureV)
    #The algorithm terminates with u and v the endpoints of the diameter
    levelStructureU, nqkakuvMaxiLevel = bfsLevel(u)
    #ALGORITHM II - minimizing level width
  
    alp = [[-1, -1] for _ in range(n+1)] #associated level pairs
    for i in verticesInThisComponent:
        alp[i] = [ levelStructureV[i], maxiLevelV - levelStructureU[i] + 1 ]

    levelN = [ [] for _ in range(0,n+1) ]
    print("n=", n)
    # step 1 - all verteces whose associated level pair is in the form (i,i) get removed from the graph
    used = (n+1) * [False]
    for w in range(1, n+1):
        if w in verticesInThisComponent:
            if alp[w][0] == alp[w][1]:
                print("alp[w][0] =",alp[w][0] )
                print("w=", w)
                levelN[ alp[w][0] ].append(w)
                used[w] = True
    print("end of ALG II step 1")
    #step 2 - Find the components and arrange them in descending order based on the number of vertices in each component
    c = [ [] for _ in range(0,n+1) ]
    def dfs(start, component):
        used[start] = True
        c[component].append(start)
        for next in edges[start]:
            if used[next] == False:
                dfs(next, component)

    component = 0
    for i in range(1, n+1):
        if used[i] == 0 and (i in verticesInThisComponent):
            component += 1
            dfs(i, component)

    next_component = [ (len(c[next]), c[next]) for next in range(0, component+1) ]
    next_component.sort()

    #step 3 - for each component do these a, b and c something

    #sm A - szLN[i] is the width of levelN[i] for now(only w nodes)
    szLN = (n+1) * [0]   # szLN[i] = size of levelN[i]
    for i in range(0, n+1):
        szLN[i] = len(levelN[i])

    #sm B - compute the vectors h and l
    h = [szLN[i] for i in range(n+1)]
    l = [szLN[i] for i in range(n+1)]

    for w in verticesInThisComponent:
        i = alp[w][0]
        j = alp[w][1]
        h[i] += 1
        l[j] += 1 #?? maxiLevelV - j + 1

    #sm C
    l0 = 0
    h0 = 0
    for i in verticesInThisComponent:
        if l[i] - szLN[i] > 0:
            if l[i] > l0:
                l0 = l[i]
        
        if h[i] - szLN[i] > 0:
            if h[i] > h0:
                h0 = h[i]

    first_or_second = -1 # sometimes in the end we have -1 for an answer/ it stays this way bc all the vertices have alp (i,i)
    for com in range(1, component+1):
        for w in next_component[com][1]:
            if alp[w][0] != alp[w][1]: # when this if is false -> first_or_second = -1
                if h0 < l0:
                    levelN[ alp[w][0] ].append(w) 
                    first_or_second = 1
                elif l0 < h0:
                    levelN[ alp[w][1] ].append(w) #?? maxiLevelV - j + 1 
                    first_or_second = 2
                else:
                    if widthV < widthU:
                        levelN[ alp[w][0] ].append(w) 
                        first_or_second = 1
                    else:
                        levelN[ alp[w][1] ].append(w) #?? maxiLevelV - j + 1 
                        first_or_second = 2

    for k in range(1, maxiLevelV+1):
        if k in verticesInThisComponent:
            print(k, ":")
            print(levelN[k])
    #ALGORITHM III -Numbering

    #A - interchange u and v if needed
    def swap(u,v):
        return v, u

    interchangedUV = False
    if len(edges[u]) < len(edges[v]):
        interchangedUV = True
        u,v = swap(u,v)

        for i in range(1, n+1):  
            if i in verticesInThisComponent:
                levelN[i] = maxiLevelV - levelN[i] + 1

    #B - numbering       

    newI[v] = num
    oldI[num] = v
    num += 1
    
    k = 0
    while (k <= maxiLevelV): # [1, maxiLevelV]
        #B2
        k += 1 
        print("k=", k)
        for ni in range(1,n+1): # [1,n]
            if oldI[ni] == 0:
                break
            if (oldI[ni] not in levelN[k]) or (oldI[ni] not in verticesInThisComponent):
                continue
            next_edges = [(len(edges[i]), i) for i in edges[oldI[ni]]]
            next_edges.sort()
            for _,next in next_edges:
                if ( num > n ):
                    break
                if newI[next] == 0:
                    print("num1=", num)
                    print("next1=", next)
                    newI[next] = num
                    oldI[num] = next
                    if ( bandwidth < num - ni ):
                        bandwidth = num - ni
                    num += 1
        #B3
        degreeUnnumbered = oo
        unnumbered = -1
        
        for w in levelN[k]:
            if newI[w] == 0:
                if len(edges[w]) < degreeUnnumbered:
                    degreeUnnumbered = len(edges[w])
                    unnumbered = w
                    print("unnumbered=", w)
        if unnumbered != -1:
            print(num)
            newI[unnumbered] = num
            oldI[num] = unnumbered
            num += 1
            k = k-1
            continue

        #C
        print("step C---------------------")
        for ni in range(1,n+1):
            if ( num > n ):
                break
            if oldI[ni] == 0:
                continue#break # continue i think
            print("in the cycle")
            if oldI[ni] in levelN[k]:
                next_edges = [(len(edges[i]), i) for i in edges[oldI[ni]]]
                next_edges.sort()
                for _,next in next_edges:
                    if ( num > n ):
                        break 
                    if next in levelN[k+1]:
                        if ( newI[next] != 0 ):
                            continue
                        print("num22222222222222222222222222222222222222222222222=", num)
                        print("next2=", next)
                        newI[next] = num
                        oldI[num] = next
                        if ( bandwidth < num - ni ):
                            bandwidth = num - ni
                        num += 1
        
    print("bandwidth before step D=", bandwidth);                 
    print(newI)
    #D 
    print("interchangedUV=", interchangedUV)
    print("first_or_second=", first_or_second)
    if (interchangedUV == True and first_or_second == 2) or (interchangedUV == False and first_or_second == 1):
        print("step D in motion")
        for i in range(1, n+1):
            if i in verticesInThisComponent:
                newI[i] = n - i + 1
        print(newI)

#printing results

