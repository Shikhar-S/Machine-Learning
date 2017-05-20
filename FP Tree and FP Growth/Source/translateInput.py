from collections import defaultdict
numberOfBins=input()
maxx=[-1,-1,-1,-1,-1,-1,-1,-1,-1]
minn=[1000,1000,1000,1000,1000,1000,1000,1000,1000]
with open("data.txt","r") as F:
	for line in F:
		x=line.split(',')
		ctr=0 
		for t in x:
			d_t=float(t)
			if(d_t==0 and ctr!=8 and ctr!=0 and ctr!=7):
				continue
			maxx[ctr]=max(maxx[ctr],d_t)
			minn[ctr]=min(minn[ctr],d_t)
			ctr+=1
maxx[6]=4
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
			if(d_t==0 and ctr!=8 and ctr!=0 and ctr!=7):
				bin=int((numberOfBins*(maxx[ctr]+minn[ctr]))/2.0)
			else:
				bin=int(((d_t-minn[ctr])/(maxx[ctr]-minn[ctr]))*(numberOfBins))
			
			d[item[ctr]+str(bin)]+=1;
			ctr+=1

with open("data.txt","r") as G:
	for line in G:
		data=list()
		print 'T'
		x=line.split(',')
		ctr=0
		item=['A','B','C','D','E','F','G','H','I','J','K']
		for t in x:
			d_t=float(t)
			bin=int(((d_t-minn[ctr])/(maxx[ctr]-minn[ctr]))*numberOfBins)
			data.append((d[item[ctr]+str(bin)],item[ctr]+str(bin)))
			S.add((d[item[ctr]+str(bin)],item[ctr]+str(bin)))
			ctr+=1
		data.sort(reverse=True)
		#print len(data)
		for x in data:
			print x[1]
print 'F'
S=sorted(S)
for x in S:
	print x[1]
print 'EOF'