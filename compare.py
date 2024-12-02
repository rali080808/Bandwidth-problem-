import time
import random
import networkx as nx
from collections import deque
from collections import defaultdict

# choosing integers for n and m

''' 
n = int(input())
m = int(input())
edges = [ [] for _ in range(n+1) ]
for j in range(0,m):
      b = int(input())
      e = int(input())
      #b += 1
      #e += 1
      edges[b].append(e)
      edges[e].append(b)
''' 
while True:

    
    l = [  i   for i in range(4, 2000)]
    n = random.choice(l)

    l = [i for i in range(int(round(n/2, 0)), n)]
    m = random.choice(l)
    
    n=1500
    g = nx.g = nx.erdos_renyi_graph(n, 0.5)
    #n= 10000
    print("n=", n)
    
    
    #print("m=", m)

    edges = [ [] for _ in range(0,n+3) ]
    for x,y in g.edges():
        x += 1
        y += 1
        #print(f"{x}, {y}")
        edges[x].append(y)
        edges[y].append(x)
    
    #GPS=================================================================================================================
    oo = 10000000

    start_time = time.time()

    newI = [0] * (n+1)
    oldI = [0] * (n+2)
    bandwidth = 0
    num = 1
    while True: # big
        
        flag = True
        for w in range(1, n+1):
            if newI[w]==0:
                flag = False
                break
        
        if flag: 
            break
        #ALGORITHM I - finding a starting vertex

        v = -1
        for i in range(1, n+1):
            if newI[i]==0:
                v = i
                break

        for i in range(1, n+1):
            if len(edges[i]) < len(edges[v]) and newI[i]==0:
                v = i

        maxiLevel = -1
        
        def bfsLevel(start):
            level = [ (-1) for _ in range(0, n+1)]
            q = deque([start])
            level[start] = 1
            maxiLevel = -1
            while q:
                curr = q.popleft()
                for next in edges[curr]:
                    #print(next, level[next])
                    if level[next] == -1: 
                        level[next] = level[curr] + 1
                        if level[next] > maxiLevel:
                            maxiLevel = level[next]
                        q.append(next)
            
            return level,maxiLevel

        def findWidth(level):
            #width = [ (0) for _ in range(0, n+1)]
            width = defaultdict(int)
            
            for l in level:
                if ( l != -1 ):
                    width[l] += 1

            maximalWidth = 0
            for l, w in width.items():
                if w > maximalWidth:
                    maximalWidth = w
            
            return maximalWidth

        verticesInThisComponent = []
        levelStructureV,maxiLevel = bfsLevel(v)
    
        for w in range(1, n+1):
            if levelStructureV[w] != -1:
                verticesInThisComponent.append(w)
        #print("vertices in this component = ", verticesInThisComponent)         

        maxiLevelV = maxiLevel
        u = -1
        flag = 1
        levelStructureU = []
        levelStructureW = [ [[], (0)] for _ in range(0, n+1) ]
        for w in verticesInThisComponent:
            nqkakuvLevelStructure, nqkakuvMaxiLevel = bfsLevel(w)
            levelStructureW[w] = [nqkakuvLevelStructure, nqkakuvMaxiLevel]

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
                #levelStructureS,maxiLevel = bfsLevel(next)
                levelStructureS = levelStructureW[next][0]
                maxiLevel = levelStructureW[next][1]
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
            flag = False

        #print('maxiLevelV=', maxiLevelV)
        #print("v=",v)
        #print("u=",u)
        widthU = minimalWidthS # izlishno, zashtoto go slozhih na line 112
        widthV = findWidth(levelStructureV)
        #The algorithm terminates with u and v the endpoints of the diameter
        levelStructureU, nqkakuvMaxiLevel = bfsLevel(u)
        #ALGORITHM II - minimizing level width
    
        alp = [[-1, -1] for _ in range(n+1)] #associated level pairs
        for i in verticesInThisComponent:
            alp[i] = [ levelStructureV[i], maxiLevelV - levelStructureU[i] + 1 ]

        levelN = [ [] for _ in range(0,n+2) ]
        #print("n=", n)
        # step 1 - all verteces whose associated level pair is in the form (i,i) get removed from the graph
        used = [(False) for _ in range(0, n+1)]
        for w in range(1, n+1):
            if w in verticesInThisComponent:
                if alp[w][0] == alp[w][1]:
                    #print("alp[w][0] =",alp[w][0] )
                    #print("w=", w)
                    levelN[ alp[w][0] ].append(w)
                    used[w] = True
        #print("end of ALG II step 1")
        #step 2 - Find the components and arrange them in descending order based on the number of vertices in each component
        c = [ [] for _ in range(0,n+1) ]
        '''
        def dfs(start, component):
            used[start] = True
            c[component].append(start)
            for next in edges[start]:
                if used[next] == False:
                    dfs(next, component)
    '''
        def dfs(start, component):
            stack = [start]
            while stack:
                curr = stack.pop()
                if used[curr]:
                    continue
                else:
                    used[curr] = True
                    c[component].append(curr)
                
                for next in reversed(edges[curr]):
                    if not used[next]:
                        stack.append(next)
        
        
        component = 0
        for i in range(1, n+1):
            if not used[i] and (i in verticesInThisComponent):
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
            l[j] += 1 #?? maxiLevelV - j + 1 #index out of range??

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
                        if widthV <= widthU:
                            levelN[ alp[w][0] ].append(w) 
                            first_or_second = 1
                        else:
                            levelN[ alp[w][1] ].append(w) #?? maxiLevelV - j + 1 
                            first_or_second = 2

        '''
        for k in range(1, maxiLevelV+1):
            if k in verticesInThisComponent:
                print(k, ":")
                print(levelN[k])
        '''
        #ALGORITHM III -Numbering

        #A - interchange u and v if needed
        def swap(u,v):
            return v, u

        interchangedUV = False
        if len(edges[u]) < len(edges[v]):
            interchangedUV = True
            u,v = swap(u,v)
            #print("interchangedUV")
            for i in range(1, maxiLevelV+1):  
                levelN[i] , levelN[maxiLevelV-i+1] = swap(levelN[i] , levelN[maxiLevelV-i+1] )

        #B - numbering       
        first_num_of_this_component = num
        newI[v] = num
        oldI[num] = v
        num += 1
        
        k = 0
        while (k <= maxiLevelV): # [1, maxiLevelV]
            #B2
            k += 1 
            #print("k=", k)
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
                    if not newI[next]:
                        #print("num1=", num)
                        #print("next1=", next)
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
                        #print("unnumbered=", w)
            if unnumbered != -1:
                #print(num)
                newI[unnumbered] = num
                oldI[num] = unnumbered
                num += 1
                k = k-1
                continue

            #C
            #print("step C---------------------")
            for ni in range(1,n+1):
                if ( num > n ):
                    break
                if oldI[ni] == 0:
                    continue#break # continue i think
                #print("in the cycle")
                if oldI[ni] in levelN[k]:
                    next_edges = [(len(edges[i]), i) for i in edges[oldI[ni]]]
                    next_edges.sort()
                    for _,next in next_edges:
                        if ( num > n ):
                            break 
                        if next in levelN[k+1]:
                            if ( newI[next] != 0 ):
                                continue
                            #print("num22222222222222222222222222222222222222222222222=", num)
                            #print("next2=", next)
                            newI[next] = num
                            oldI[num] = next
                            if ( bandwidth < num - ni ):
                                bandwidth = num - ni
                            num += 1
            
        #print("bandwidth before step D=", bandwidth);                 
        #print(newI)
        #D 
        #print("interchangedUV=", interchangedUV)
        #print("first_or_second=", first_or_second)
        
        if (interchangedUV == True and first_or_second == 2) or (interchangedUV == False and first_or_second == 1):
            #print("step D in motion")
            for i in range(1, n+1):
                if i in verticesInThisComponent:
                    newI[i] = first_num_of_this_component + first_num_of_this_component - 1 + len(verticesInThisComponent) - newI[i]  #neeeeeeeeeeeeee
            
            s = verticesInThisComponent[0]
            q = deque()
            q.append(s)
            b = 0
            used = [(False) for _ in range(0, n+1)]
            while q:
                curr = q.pop()
                for next in edges[curr]:
                    if not used[next]:
                        used[next] = True
                        if newI[next] > newI[curr] and newI[next] - newI[curr] > b:
                            b = newI[next] - newI[curr]
                        elif newI[curr] > newI[next] and newI[curr] - newI[next] > b:
                            b = newI[curr] - newI[next]
                        q.append(next)
            if b < bandwidth:
                bandwidth = b
            #print(newI)

    #printing results

    #print(newI)
    print("bandwidth=", bandwidth)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"execution time for GPS = {execution_time}")
    #CMK================================================================================================================================

    
    import random 
    MAXN = 100000

    start_time = time.time()


    comp = [0] * (n+1)
    components = 0

    '''
    def dfs(start, component):
        comp[start] = component
        for next in edges[start]:
                if comp[next] == 0:
                    dfs(next, component)
    '''

    def dfs(start, component):
        stack = [start]
        while stack:
            curr = stack.pop()
            if comp[curr]:
                continue
            comp[curr] = component
            for next in reversed(edges[curr]):
                if comp[next] == 0:
                    stack.append(next)


    for w in range(1, n+1):
        if comp[w] == 0:
                components += 1
                dfs(w, components)


    nums = [-1] * (n+1)
    answerBandwidth = -1
    thisComp = 1
    last = 1
    while thisComp <= components:
        
        #finding the vertices with minimal degree
        minDeg = oo
        for i in range(1, n+1):
                if len(edges[i]) < minDeg and comp[i] == thisComp:
                    minDeg = len(edges[i])
                    #print(minDeg)
        minDegreeNodes = [ node for node in range(1, n+1) if len(edges[node]) == minDeg and comp[node] == thisComp ]
        
        #print("minDegreeNodes=", minDegreeNodes)
        
        k = 1
        smallestBandwidth = n
        newnum = last
        for r in range(min(k, len(minDegreeNodes))):
                s=0
                if len(minDegreeNodes) <= k:
                    s = minDegreeNodes[r]
                else:
                    #print("random")
                    s = random.choice(minDegreeNodes)
                
                #print("checknums=", nums)
                currnums = nums.copy()
                #print("checknums=", nums)
                q = deque([s])
                currnums[s] = last
                newnum = last+1
                visited = [False] * (n+1) # ne bash taka ama ne prechi
                    
                visited[s] = True
                bandwidth = -1
                while(q):
                    curr = q.popleft() 
                    #print("curr=", curr)
                    #print("whilenums", nums)
                    next_edges = [(len(edges[next]), next) for next in edges[curr]]
                    next_edges.sort()
                    for _, next in next_edges:
                            if visited[next]==False:
                                q.append(next)
                                visited[next] = True
                                currnums[next] = newnum
                                newnum = newnum + 1
                                if bandwidth < currnums[next] - currnums[curr]:
                                        bandwidth = currnums[next] - currnums[curr]
                                        #print("if bandwidth", bandwidth)
                                        #print("if nums=", nums)
                                
                #print('currBandwidth=',bandwidth)
                if bandwidth <= smallestBandwidth:
                    smallestBandwidth = bandwidth
                    #print("smallestbandwidth=",smallestBandwidth)
                    nums = currnums.copy()
                    #print("newnumsss=", currnums)
        if smallestBandwidth > answerBandwidth:
                answerBandwidth = smallestBandwidth
                #print("answerbandwidth=",answerBandwidth)
        
        last = newnum
        thisComp += 1
    

    #print(nums)
    print("bandwidth=",answerBandwidth)


    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time for CMK = {execution_time} seconds") 