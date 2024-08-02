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
minDegreeNodes = []
for i in range(1,n+1):
      if ( len(edges[i]) < p ):
            p = len(edges[i])
            minDegreeNodes = [i]
      elif len(edges[i]) == p:
            minDegreeNodes.append(i)

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
            s = random.choice(minDegreeNodes)
      
      currnums = []
      for i in range(0, n+1):
            currnums.append(-1)
            
      newnum = 2
      q = [s]
      currnums[s] = 1
      visited = []
      for i in range(MAXN):
            visited.append(0)
            
      visited[s] = True
      bandwidth = -1
      while(len(q)!=0):
            curr = q[0]
            curr = q[0]
            del(q[0])
            next_edges = [(len(edges[next]), next) for next in edges[curr]]
            next_edges.sort()
            for _, next in next_edges:
                  if visited[next]==False:
                        q.append(next)
                        visited[next] = True
                        currnums[next] = newnum
                        if bandwidth < newnum - currnums[curr]:
                              bandwidth = newnum - currnums[curr]
                        newnum = newnum + 1
      #print('currBandwidth=',bandwidth)
      if bandwidth <= smallestBandwidth:
            smallestBandwidth = bandwidth
            #print("hibandwidth=",smallestBandwidth)
            nums = currnums
 

print(nums)
print("bandwidth=",smallestBandwidth)
