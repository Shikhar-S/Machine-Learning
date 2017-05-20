import sys
from collections import defaultdict
item=['A','B','C','D','E','F','G','H','I','J','K']
with open("g.txt","r") as G:
	for line in G:
		flag=0
		items=line.split(' ')
		i=0
		for x in items:
			i+=1
			if(x==('')):
				continue
			if(x.startswith('#')):
				print x,
				flag=1
				continue
			if(flag==1):
				print x,
				break
			vv=int(item.index(x[0])+1)*10+int(x[1])
			vv=str(vv)
			if(i!=len(items)-2):
				vv+=','
			else:
				vv+=' '
			sys.stdout.write(vv)