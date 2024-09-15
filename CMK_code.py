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


p = 100000000
minDeg = m
for i in range(1, n+1):
      if ( len(edges[i]) < minDeg ):
            minDeg = len(edges[i])
            print(minDeg)
minDegreeNodes = [ node for node in range(1, n+1) if len(edges[node]) == minDeg ]
 
print("minDegreeNodes=", minDegreeNodes)
nums = []
for i in range(0, n+1):
      nums.append(-1)

k = 8
smallestBandwidth = n
if len(minDegreeNodes) < k:
      k = len(minDegreeNodes)

for r in range(k):
      s=0
      if len(minDegreeNodes) <= k:
            s = minDegreeNodes[r]
      else:
            print("random")
            s = random.choice(minDegreeNodes)
      
      currnums = []
      for i in range(0, n+1):
            currnums.append(-1)
            
      newnum = 2
      q = [s]
      currnums[s] = 1
      visited = [False] * (n+1)
            
      visited[s] = True
      bandwidth = -1
      while(q):
            curr = q[0] 
            print("curr=", curr)
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
                        
      print('currBandwidth=',bandwidth)
      if bandwidth <= smallestBandwidth:
            smallestBandwidth = bandwidth
            print("hibandwidth=",smallestBandwidth)
            nums = currnums
 

print(nums)
print("bandwidth=",smallestBandwidth)
