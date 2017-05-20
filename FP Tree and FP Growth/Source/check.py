from collections import defaultdict
maxx=[-1,-1,-1,-1,-1,-1,-1,-1,-1]
minn=[1000,1000,1000,1000,1000,1000,1000,1000,1000]
with open("data.txt","r") as F:
	for line in F:
		x=line.split(',')
		ctr=0
		for t in x:
			d_t=float(t)
			maxx[ctr]=max(maxx[ctr],d_t)
			minn[ctr]=min(minn[ctr],d_t)
			ctr+=1
d={}
d=defaultdict(lambda:0,d)
S=set()
with open("data.txt","r") as G:
	for line in G:
		x=line.split(',')
		ctr=0
		item=['A','B','C','D','E','F','G','H','I','J','K']
		for t in x:
			d_t=float(t)
			bin=int((d_t-minn[ctr])/(maxx[ctr]-minn[ctr])*10)
			d[item[ctr]+str(bin)]+=1;
			ctr+=1
t=0
for x in d:
	print x, d[x]
	t+=d[x]

print "Total ele=",t