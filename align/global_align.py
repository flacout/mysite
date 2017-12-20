from numpy import *
import time

def makeAlignment(sequence1,sequence2):
    global sequenceA
    global sequenceB
    sequenceA = sequence1
    sequenceB = sequence2
    # settup a matrix of integers fill with 0, and of lenght n+1 column, m+1 rows 
    # (sequence A horizontal, sequenceB vertical).
    # Scoring matrice: with score match 2, mismatch -1, gap -1.
    # traceBackMatrix: where diagonalarrow=1 uparrow=2 horozontalarrow=3
    n=len(sequenceA)
    m=len(sequenceB)
    scoreMatrix=array([0]*((m+1)*(n+1)),dtype=int).reshape((m+1),(n+1))
    traceBackMatrix=array([0]*((m+1)*(n+1)),dtype=int).reshape((m+1),(n+1))

    scoreMatrix, traceBackMatrix = fillMatrices(scoreMatrix, traceBackMatrix, 
                                                n, m)
    # find coordinates of the starting point of our best paths
    i, j = findOrigin(scoreMatrix)
    # Create the 3 strings to print the result
    sequence3A, trace, sequence3B = followTraceBack(scoreMatrix, traceBackMatrix, 
                                                    i, j)
    result = formatOutput(sequence3A, trace, sequence3B)
    return result


def fillMatrices(scoreMatrix, traceBackMatrix, n, m):
	#filling array values
	i=1
	while i<=m:
		j=1
		while j<=n:
			if sequenceA[j-1]==sequenceB[i-1]: match=2
			else: match=-1
			diagonal=scoreMatrix[i-1,j-1]+match
			row=max(scoreMatrix[i,:j])-1
			column=max(scoreMatrix[:i,j])-1
			score=max(diagonal,row,column)
			scoreMatrix[i,j]=score
			if score==diagonal: traceBackMatrix[i,j]=1
			elif score==row: traceBackMatrix[i,j]=3
			elif score==column: traceBackMatrix[i,j]=2
			
			j+=1
		i+=1
	return scoreMatrix, traceBackMatrix

def findOrigin(scoreMatrix):
    origin=amax(scoreMatrix)
    cells=where(scoreMatrix==origin)
    i=cells[0][0]
    j=cells[1][0]
    return i,j

def followTraceBack(scoreMatrix, traceBackMatrix, i, j):
	sequence3A=''
	trace=''
	sequence3B=''

	while i!=0 and j!=0:
		if traceBackMatrix[i,j]==3 :
			sequence3A+=sequenceA[j-1]
			sequence3B+='-'
			trace+=' '
			j-=1
		elif traceBackMatrix[i,j]==2:
			sequence3A+='-'
			sequence3B+=sequenceB[i-1]
			trace+=' '
			i-=1
		elif traceBackMatrix[i,j]==1:
			sequence3A+=sequenceA[j-1]
			sequence3B+=sequenceB[i-1]
			if scoreMatrix[i,j]==scoreMatrix[i-1,j-1]+2 : trace+='|'
			else: trace+='*'
			i-=1
			j-=1

	# Add rest of the sequence if alignment doesn't start from the beginning
	sequence3A, trace, sequence3B = addTraillingSequence(sequence3A, trace, sequence3B,
                                                         i, j)
	return sequence3A, trace, sequence3B

def addTraillingSequence(sequence3A, trace, sequence3B, i, j):
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
	return sequence3A, trace, sequence3B

def formatOutput(sequence3A, trace, sequence3B):
	# Reverse the string to display the result.
	# Because we have analysed the matrix from the 'bottom' of it
	# And create one string for the final result
	sequence3A=sequence3A[::-1]
	trace=trace[::-1]
	sequence3B=sequence3B[::-1]
	result=''
	startRow=0
	endRow=50
	while startRow<len(trace):
		result+=sequence3A[startRow:endRow]+"\n"
		result+=trace[startRow:endRow]+"\n"
		result+=sequence3B[startRow:endRow]+"\n"+"\n"
		startRow+=50
		endRow+=50
	return result



if __name__=="__main__":
    start_time = time.time()
    sequence1='MKFLSARDFQPVAFLGLMLLTATAFPTSQVRRGDFTEDTTHNRPVYTTSQVGGLITYVLREILEMRKELCNGNSDCMNSDDALSENNLKLPEIQRNDGCFQTGYNQEICLLKICSGLLEFRFYLEFVKNNLQDNKKDKARVIQSNTETLVHIFKQEIKDSYKIVLPTPTSNALLMEKLESQKEWLRTKTIQLILKALEEFLKVTMRSTRQT'
    sequence2='MKFLSARDFHPVAFLGLMLVTTTAFPTSQVRRGDFTEDTTPNRPVYTTSQVGGLITHVLWEIVEMRKELCNGNSDCMNNDDALAENNLKLPEIQRNDGCYQTGYNQEICLLKISSGLLEYHSYLEYMKNNLKDNKKDKARVLQRDTETLIHIFNQEVKDLHKIVLPTPISNALLTDKLESQKEWLRTKTIQFILKSLEEFLKVTLRSTRQT'
    #sequenceA="TAATGCATGGCGGGTG"
    #sequenceB="CCGTTATGCGGGAG"
    #presequenceA=open('seqtest1','r').read()
    #presequenceB=open('seqtest2','r').read()
    print (makeAlignment(sequence1,sequence2))
    print ("--- %s seconds ---" % (time.time() - start_time))