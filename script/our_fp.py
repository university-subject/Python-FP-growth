from itertools import combinations
import sys

class FPNode:
  def __init__(self,item, count=1, parent=None, next=None):
    self.item=item
    self.count=count
    self.children=dict()
    self.parent=parent
    self.next=next

def add_fp_tree(num, fp_tree, i, fp_map, times):
  if i>=len(num):
    return
  if num[i] not in fp_tree.children:
    fp_tree.children[num[i]]=FPNode(num[i])
    fp_tree.children[num[i]].parent=fp_tree
    fp_tree.children[num[i]].count=times
    if num[i] not in fp_map:
      fp_map[num[i]]=[times, fp_tree.children[num[i]], fp_tree.children[num[i]]]
    else:
      fp_map[num[i]][0]+=times
      fp_map[num[i]][2].next=fp_tree.children[num[i]]
      fp_map[num[i]][2]=fp_tree.children[num[i]]
      fp_tree.children[num[i]].next=None
  else:
    fp_tree.children[num[i]].count+=times
    fp_map[num[i]][0]+=times
  add_fp_tree(num, fp_tree.children[num[i]], i+1, fp_map, times)

def get(fp_tree, num):
  if fp_tree==None or fp_tree.item==-1:return
  num.append(fp_tree.item)
  get(fp_tree.parent, num)

def caculate(fp_tree, data):
  if fp_tree==None or fp_tree.item==-1:
    return
  temp=[]
  get(fp_tree, temp)
  temp.pop(0)
  if len(temp)==0:
    return
  if tuple(temp) not in data:
    data[tuple(temp)]=fp_tree.count
  caculate(fp_tree.next, data)

def count_data(data, mp):
  for k in data:
    for r in k:
      if r not in mp:
        mp[r]=data[k]
      else:
        mp[r]+=data[k]
def fp_dfs(data, temp_ans, ans, frequency):
  if len(data)==0:
    return
  mp=dict()
  count_data(data, mp)
  fp_tree=FPNode(-1)
  fp_tree_next=dict()
  for k in data:
    times = data[k]
    k = list(k)
    k.sort(key=lambda x:mp[x], reverse=True)
    for i in range(len(k)-1, -1, -1):
      if mp[k[i]]<813:
        k.pop()
      else:
        break
    add_fp_tree(k, fp_tree, 0, fp_tree_next, times)  
  fp_tree_next = sorted(fp_tree_next.items(),key=lambda x:x[1][0])
  for k in fp_tree_next:
    next_data={}
    temp_ans.append(k[0])
    if len(temp_ans)<=5:
      ans[len(temp_ans)-1]+=1
      frequency[len(temp_ans)-1][frozenset(temp_ans)]=k[1][0]
      caculate(k[1][1], next_data)
      fp_dfs(next_data, temp_ans, ans, frequency)
    temp_ans.pop()

sys.setrecursionlimit(2000)
f = open('test_data/mushroom.dat', 'r')
data = {}
for line in iter(f):
  line=tuple(map(int, str(line).split()))
  if line not in data:
    data[line]=1
  else:
    data[line]+=1
ans=[0]*5
frequency=[dict() for i in range(5)]
fp_dfs(data, [], ans, frequency)
print(ans)
association_rule=0
for i in range(4,0,-1):
  for k in frequency[i]:
    for j in range(1,i+1):
      for s in combinations(k, j):
        if frequency[i][k]/frequency[j-1][frozenset(s)]>=0.8:
          association_rule+=1
print(association_rule)