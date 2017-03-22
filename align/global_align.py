from numpy import *
from DNA_sequence import *
import time

def Alignment(sequenceA,sequenceB):

	n=len(sequenceA)
	m=len(sequenceB)
	
	'''
	settup a matrix of integers fill with 0, and of lenght n+1 column, m+1 rows 
	(sequence A horizontal, sequenceB vertical).
	Scoring matrice: with score match 2, mismatch -1, gap -1.
	paths matrix2: where diagonalarrow=1 uparrow=2 horozontalarrow=3
	'''
	MAT=array([0]*((m+1)*(n+1)),dtype=int).reshape((m+1),(n+1))
	MAT2=array([0]*((m+1)*(n+1)),dtype=int).reshape((m+1),(n+1))

	#filling array values
	i=1
	while i<=m:
		j=1
		while j<=n:
			if sequenceA[j-1]==sequenceB[i-1]: match=2
			else: match=-1
			diagonal=MAT[i-1,j-1]+match
			row=max(MAT[i,:j])-1
			column=max(MAT[:i,j])-1
			score=max(diagonal,row,column)
			MAT[i,j]=score
			if score==diagonal: MAT2[i,j]=1
			elif score==row: MAT2[i,j]=3
			elif score==column: MAT2[i,j]=2
			
			j+=1
		i+=1
	#print MAT
	#print MAT2

	#set up origin points of the different paths
	origin=amax(MAT)
	cells=where(MAT==origin)

	i=cells[0][0]
	j=cells[1][0]

	# Create the 3 strings to print the result
	# According to the path Matrix
	sequence3A=''
	trace=''
	sequence3B=''

	while i!=0 and j!=0:
		if MAT2[i,j]==3 :
			sequence3A+=sequenceA[j-1]
			sequence3B+='-'
			trace+=' '
			j-=1
		elif MAT2[i,j]==2:
			sequence3A+='-'
			sequence3B+=sequenceB[i-1]
			trace+=' '
			i-=1
		elif MAT2[i,j]==1:
			sequence3A+=sequenceA[j-1]
			sequence3B+=sequenceB[i-1]
			if MAT[i,j]==MAT[i-1,j-1]+2 : trace+='|'
			else: trace+='*'
			i-=1
			j-=1

	# Add rest of the sequence if alignment doesn't start from the beginning
	while j>0:
			sequence3A+=sequenceA[j-1]
			sequence3B+='-'
			trace+=' '
			j-=1
	while i>0:
		sequence3A+='-'
		sequence3B+=sequenceB[i-1]
		trace+=' '
		i-=1

	# Reverse the string to display the result.
	# Because we have analysed the matrix from the 'bottom' of it
	# And create one string for the final result
	sequence3A=sequence3A[::-1]
	trace=trace[::-1]
	sequence3B=sequence3B[::-1]

	result=''
	debut=0
	fin=50
	while debut<len(trace):
		result+=sequence3A[debut:fin]+"\n"
		result+=trace[debut:fin]+"\n"
		result+=sequence3B[debut:fin]+"\n"+"\n"
		debut+=50
		fin+=50

	return result



if __name__=="__main__":
	start_time = time.time()
	sequenceA='MKFLSARDFQPVAFLGLMLLTATAFPTSQVRRGDFTEDTTHNRPVYTTSQVGGLITYVLREILEMRKELCNGNSDCMNSDDALSENNLKLPEIQRNDGCFQTGYNQEICLLKICSGLLEFRFYLEFVKNNLQDNKKDKARVIQSNTETLVHIFKQEIKDSYKIVLPTPTSNALLMEKLESQKEWLRTKTIQLILKALEEFLKVTMRSTRQT'
	sequenceB='MKFLSARDFHPVAFLGLMLVTTTAFPTSQVRRGDFTEDTTPNRPVYTTSQVGGLITHVLWEIVEMRKELCNGNSDCMNNDDALAENNLKLPEIQRNDGCYQTGYNQEICLLKISSGLLEYHSYLEYMKNNLKDNKKDKARVLQRDTETLIHIFNQEVKDLHKIVLPTPISNALLTDKLESQKEWLRTKTIQFILKSLEEFLKVTLRSTRQT'
	#sequenceA="TAATGCATGGCGGGTG"
	#sequenceB="CCGTTATGCGGGAG"
	#presequenceA=open('seqtest1','r').read()
	#sequenceA=FastaDNA(presequenceA).sequence
	#presequenceB=open('seqtest2','r').read()
	#sequenceB=FastaDNA(presequenceB).sequence
	print Alignment(sequenceA,sequenceB)
	print("--- %s seconds ---" % (time.time() - start_time))