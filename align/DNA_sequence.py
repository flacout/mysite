'''
FastaDNA is an object for DNA sequences in FASTA format.

It has two attributes:
name, for he name of the sequence.
sequence, which is the DNA sequence itself.

It has three methods:

translate(frame):
return a string with the translation of the DNA sequence into a protein sequence.
It allow the 3 different reading frame to be operated.

If frame=2, the translation begin at the second base.
If frame=3, the translation begin at the third base.
For every other value of frame, the translation begin at the first base.

reverse():
takes no argument and return a string with the DNA sequence reversed.

reverse_complement():
takes no argument and return a string with the complementary strand of DNA reversed.
'''

import re

class FastaDNA:
	def __init__(self,fasta):
		self.fasta=fasta

		# initialize the name of the FASTA file
		name1=re.findall('>(.+?)\n',self.fasta)[0]
		self.name=name1.strip()

		# initialyse the sequence of the FASTA file
		self.sequence=self.get_sequence()

		# All the possible codon and their amino acid
		self.codontable={'TTT':'F','TTC':'F','TTA':'L','TTG':'L','CTT':'L','CTC':'L','CTA':'L','CTG':'L','ATT':'I','ATC':'I','ATA':'I','ATG':'M','GTT':'V','GTC':'V','GTA':'V','GTG':'V'
		           		,'TCT':'S','TCC':'S','TCA':'S','TCG':'S','CCT':'P','CCC':'P','CCA':'P','CCG':'P','ACT':'T','ACC':'T','ACA':'T','ACG':'T','GCT':'A','GCC':'A','GCA':'A','GCG':'A'
		           		,'TAT':'Y','TAC':'Y','TAA':'*','TAG':'*','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q','AAT':'N','AAC':'N','AAA':'K','AAG':'K','GAT':'D','GAC':'D','GAA':'E','GAG':'E'
		           		,'TGT':'C','TGC':'C','TGA':'*','TGG':'W','CGT':'R','CGC':'R','CGA':'R','CGG':'R','AGT':'S','AGC':'S','AGA':'R','AGG':'R','GGT':'G','GGC':'G','GGA':'G','GGG':'G'}



	def get_sequence(self):
		# I use the regular expression to extract the DNA sequence 
		# by eliminating the name and the newlines

		sequence=''
		liste=re.findall('\n(.+)',self.fasta)
		for i in liste:
			sequence+=i.strip().upper()
		sequence=sequence.strip()
		return sequence

	def translate(self,*frame):
		# Check if an argument is passed and what argument it is
		# then apply the codon tabe for translation

		translation=''
		try :
			if frame[0]==2: i=1
			elif frame[0]==3: i=2
			else : i=0
		except : i=0
		while i<len(self.sequence):
			codon=self.sequence[i:i+3]
			try: aa=self.codontable[codon]
			except: aa='X'
			translation+=aa
			i+=3
		return translation

	def reverse(self):
		return self.sequence[::-1]

	def reverse_complement(self):
		# use the reverse method
		# then convert every base to it corresponding base on the complementary strand
		
		rev_com=''
		rev=self.reverse()
		for i in rev:
			if i=='A': rev_com+='T'
			if i=='T': rev_com+='A'
			if i=='G': rev_com+='C'
			if i=='C': rev_com+='G'
		return rev_com


if __name__=="__main__":
	sequence=open('seqtest1').read()
	sequence=FastaDNA(sequence)
	print sequence.name
	print sequence.sequence+"\n"
	print sequence.translate()+"\n"
	print sequence.translate(2)+"\n"
	print sequence.reverse()+"\n"
	print sequence.reverse_complement()