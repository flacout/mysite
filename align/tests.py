# !!! Note to myself : the method in test classes have to start with test in order to run !!!

from django.test import TestCase

import global_align as ga
from DNA_sequence import FastaDNA


class AlignmentMethodTest(TestCase):

    def test_two_equals_DNA_sequences(self):
        """
        makeAlignment of the two sequence should return True compare to
        a correct string answer.
        """
        DNAsequenceA="ATCGATAGACACAGATAGACACGAT"
        DNAsequenceB="ATCGATAGACACAGATAGACACGAT"
        correctResultAB="ATCGATAGACACAGATAGACACGAT\n|||||||||||||||||||||||||\nATCGATAGACACAGATAGACACGAT\n\n"

        programResultAB = ga.makeAlignment(DNAsequenceA, DNAsequenceB)
        
        self.assertEqual(programResultAB, correctResultAB)


    def test_two_DNA_sequences_with_mismatch(self):
        """
        makeAlignment of the two sequence should return True compare to
        a correct string answer.
        """
        DNAsequenceA="ATCGATAGACACAGATAGACACGAT"
        DNAsequenceC="ATCGATAGACATAGATAGACACGAT"
        correctResultAC="ATCGATAGACACAGATAGACACGAT\n|||||||||||*|||||||||||||\nATCGATAGACATAGATAGACACGAT\n\n"

        programResultAC = ga.makeAlignment(DNAsequenceA, DNAsequenceC)
        
        self.assertEqual(programResultAC, correctResultAC)

    def test_two_DNA_sequences_with_gap(self):
        """
        makeAlignment of the two sequence should return True compare to
        a correct string answer.
        """
        DNAsequenceA="ATCGATAGACACAGATAGACACGAT"
        DNAsequenceD="ATCGACACAGATAGACACGAT"
        correctResultAD="ATCGATAGACACAGATAGACACGAT\n|||    ||||||||||||||||||\nATC----GACACAGATAGACACGAT\n\n"

        programResultAD = ga.makeAlignment(DNAsequenceA, DNAsequenceD)
        
        self.assertEqual(programResultAD, correctResultAD)

    def test_string_format_for_long_alignment_result(self):
        """
        makeAlignment of the two sequence should return True compare to
        a correct string answer.
        """
        FastaSequenceA=open('./align/seqtest1.txt','r').read()
        DNAsequenceA=FastaDNA(FastaSequenceA).sequence
        FastaSequenceB=open('./align/seqtest2.txt','r').read()
        DNAsequenceB=FastaDNA(FastaSequenceB).sequence
        correctResult=open('./align/result.txt','r').read()


        programResult = ga.makeAlignment(DNAsequenceA, DNAsequenceB)
        
        self.assertEqual(programResult, correctResult)
