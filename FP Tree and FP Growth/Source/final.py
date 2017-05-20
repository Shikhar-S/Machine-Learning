from collections import defaultdict
numberOfBins=input()
maxx=[-1,-1,-1,-1,-1,-1,-1,-1,-1]
minn=[1000,1000,1000,1000,1000,1000,1000,1000,1000]
item=['A','B','C','D','E','F','G','H','I','J','K']
l_items=['Number of times pregnant ','Plasma glucose concentration  a 2 hours in an oral glucose tolerance test ','Diastolic blood pressure (mm Hg) ','Triceps skin fold thickness (mm) ','2-Hour serum insulin (mu U/ml) ','Body mass index (weight in kg/(height in m)^2) ','Diabetes pedigree function ','Age (years) ','Class variable']
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

with open('i.txt','r') as H:
	for line in H:
		print '-------------------------------------------------------------------------------------------------------------------'
		x=line.split(',')
		
		left=x[0].split(' ')
		right=x[1].split(' ')
		left=left[:len(left)-1]
		right=right[1:len(right)-1]
		
		for l in left:
			idx=int(l[0])-1
			val=l[1:]
			val_l=float(val)/(numberOfBins)
			val_u=(float(val)/numberOfBins)+(1.0/numberOfBins)
			if(idx==8):
				print l_items[idx],'=',int(val_l)
				continue
			print (minn[idx]+val_l*(maxx[idx]-minn[idx])),"<=",l_items[idx],'<',(minn[idx]+val_u*(maxx[idx]-minn[idx])),';',
		print '------->',
		for r in right:
			idx=int(r[0])-1
			val=r[1:]
			val_l=float(val)/(numberOfBins)
			val_u=(float(val)/numberOfBins)+(1.0/numberOfBins)
			if(idx==8):
				print l_items[idx],'=',int(val_l)
				continue
			
			print (minn[idx]+val_l*(maxx[idx]-minn[idx])),"<=",l_items[idx],'<',(minn[idx]+val_u*(maxx[idx]-minn[idx])),';'
			
