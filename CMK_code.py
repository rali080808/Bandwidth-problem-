# import networkx as nx
import random 

MAXN = 100000

n = int(input())
m = int(input())
edges = []
for i in range(n+1):
      edges.append([])
'''
g = nx.gnm_random_graph(n, m)

for x in range(1000):
    edges.append([])
 
for x,y in g.edges():
      edges[x].append(y)
      edges[y].append(x)

'''

for j in range(m):
      b = int(input())
      e = int(input())
      edges[b].append(e)
      edges[e].append(b)

comp = [0] * (n+1)
components = 0

def dfs(start, component):
      comp[start] = component
      for next in edges[start]:
            if comp[next] == 0:
                  dfs(next, component)

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
      minDeg = m
      for i in range(1, n+1):
            if len(edges[i]) < minDeg and comp[i] == thisComp:
                  minDeg = len(edges[i])
                  print(minDeg)
      minDegreeNodes = [ node for node in range(1, n+1) if len(edges[node]) == minDeg and comp[node] == thisComp ]
      
      print("minDegreeNodes=", minDegreeNodes)
      
      k = 8
      smallestBandwidth = n
      newnum = last
      for r in range(min(k, len(minDegreeNodes))):
            s=0
            if len(minDegreeNodes) <= k:
                  s = minDegreeNodes[r]
            else:
                  print("random")
                  s = random.choice(minDegreeNodes)
            
            print("checknums=", nums)
            currnums = nums.copy()
            print("checknums=", nums)
            q = [s]
            currnums[s] = last
            newnum = last+1
            visited = [False] * (n+1) # ne bash taka ama ne prechi
                  
            visited[s] = True
            bandwidth = -1
            while(q):
                  curr = q[0] 
                  print("curr=", curr)
                  print("whilenums", nums)
                  del(q[0])
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
                                    print("if bandwidth", bandwidth)
                                    print("if nums=", nums)
                              
            print('currBandwidth=',bandwidth)
            if bandwidth <= smallestBandwidth:
                  smallestBandwidth = bandwidth
                  print("smallestbandwidth=",smallestBandwidth)
                  nums = currnums.copy()
                  print("newnumsss=", currnums)
      if smallestBandwidth > answerBandwidth:
            answerBandwidth = smallestBandwidth
            print("answerbandwidth=",answerBandwidth)
      
      last = newnum
      thisComp += 1
 

print(nums)
print("bandwidth=",answerBandwidth)
