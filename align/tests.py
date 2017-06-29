# !!! Note to myself : the method in test classes have to start with test in order to run !!!

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

import align.global_align as ga
from align.DNA_sequence import FastaDNA

from .models import Alignment



def setupUser(self):
    user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
    self.client.login(username='temporary', password='temporary')
    Alignment.objects.create(alignment_name="adn1/adn2",
                             alignment_result="TTT\n|||\nTTT\n\n", 
                             user_id=user.id)
    Alignment.objects.create(alignment_name="3/4",
                             alignment_result="ATT\n|||\nATT\n\n", 
                             user_id=user.id)
    return user

def setupUserTenAlignments(self):
    user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
    self.client.login(username='temporary', password='temporary')

    for i in range(10):
        name = "name %d" % (i)
        result = "AT"*i
        q=Alignment.objects.create(alignment_name=name,
                             alignment_result=result, 
                             user_id=user.id)
    return user



class AlignmentMethodTest(TestCase):

    #----------------------------------------------------------------------------------------
    # Tests for the global_alignment.makeAlignment function.
    #----------------------------------------------------------------------------------------

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


    #----------------------------------------------------------------------------------------
    # Tests for the align:accountResults view.
    #----------------------------------------------------------------------------------------

    def test_allresults_view_with_two_alignment(self):
        user = setupUser(self)

        response = self.client.get('/align/allresults/')
        userAlignments = response.context['alignments']
        userAlignResult = userAlignments[0].alignment_result
        correctResult = "ATT\n|||\nATT\n\n"

        self.assertEqual(userAlignResult, correctResult)
        self.assertQuerysetEqual( userAlignments, 
                                ['<Alignment: 3/4>', '<Alignment: adn1/adn2>'])


    def test_allresults_view_with_deleted_alignment(self):
        user = setupUser(self)

        resultPage = self.client.post('/align/allresults/', 
                                     {'alignmentCheckbox':['1']} )

        userAlignments = resultPage.context['alignments']
        self.assertQuerysetEqual( userAlignments, ['<Alignment: 3/4>'])

    def test_allresults_view_with_unmatch_search(self):
        user = setupUser(self)

        resultPage = self.client.post('/align/allresults/', 
                                     {'search':'blabla'} )

        self.assertContains(resultPage, "No match for your search")

    def test_allresults_view_with_matching_search(self):
        user = setupUser(self)

        resultPage = self.client.post('/align/allresults/', 
                                     {'search':'adn'} )
        userAlignments = resultPage.context['alignments']

        self.assertQuerysetEqual( userAlignments, 
                                ['<Alignment: adn1/adn2>'])

    def test_allresults_view_with_new_result_created(self):
        user = setupUser(self)

        resultPage = self.client.post('/align/allresults/', 
                                     {'name_align':'5/6',
                                      'result_align':'ATTAT'} )
        userAlignments = resultPage.context['alignments']

        self.assertQuerysetEqual( userAlignments, 
                                ['<Alignment: 5/6>',
                                 '<Alignment: 3/4>', 
                                 '<Alignment: adn1/adn2>'])

    def test_allresults_view_with_multiple_alignments(self):
        user = setupUserTenAlignments(self)

        response = self.client.get('/align/allresults/')
        userAlignments = response.context['alignments']
        self.assertEqual(len(userAlignments), 5)

        responsePage2 = self.client.get('/align/allresults/2/')
        userAlignmentsPage2 = responsePage2.context['alignments']
        self.assertQuerysetEqual( userAlignmentsPage2, 
                                ['<Alignment: name 4>',
                                 '<Alignment: name 3>', 
                                 '<Alignment: name 2>',
                                 '<Alignment: name 1>',
                                 '<Alignment: name 0>'])



    #----------------------------------------------------------------------------------------
    # Test for the align:result view.
    #----------------------------------------------------------------------------------------

    def test_result_page_with_two_sequences(self):
        resultPage = self.client.post('/align/result/', 
                                     {'sequenceA':'>1\nTTAGG','sequenceB':'>2\nTTAGG'})
        name_alignment = resultPage.context['name_alignment']
        result_alignment = resultPage.context['result_alignment']

        self.assertEqual(name_alignment, "1/2")
        self.assertEqual(result_alignment, "TTAGG\n|||||\nTTAGG\n\n")

    def test_result_page_with_one_sequences_and_one_file(self):
        resultPage = self.client.post('/align/result/', 
                                     {'sequenceA':'>1\nTTAGG',
                                      'fileB':open('./align/seqtest3.txt','r')} )
        name_alignment = resultPage.context['name_alignment']
        result_alignment = resultPage.context['result_alignment']

        self.assertEqual(name_alignment, "1/gi")
        self.assertEqual(result_alignment, "-TTAG\n * ||\nAA-AG\n\n")

    def test_result_page_with_one_sequences_and_one_file(self):
        resultPage = self.client.post('/align/result/', 
                                     {'fileA':open('./align/seqtest4.txt','r'),
                                      'fileB':open('./align/seqtest3.txt','r') } )
        name_alignment = resultPage.context['name_alignment']
        result_alignment = resultPage.context['result_alignment']

        self.assertEqual(name_alignment, "seq4/gi")
        self.assertEqual(result_alignment, "AAAGAA\n||||||\nAAAGAA\n\n")

    def test_result_page_with_one_sequences(self):
        resultPage = self.client.post('/align/result/', 
                                     {'sequenceA':'>1\nTTAGG'})
        result_alignment = resultPage.context['result_alignment']

        self.assertEqual(result_alignment, "Error: You need to submit exactly 2 sequences")

    def test_result_page_with_one_file(self):
        resultPage = self.client.post('/align/result/', 
                                     {'fileA':open('./align/seqtest1.txt','r')})
        result_alignment = resultPage.context['result_alignment']

        self.assertEqual(result_alignment, "Error: You need to submit exactly 2 sequences")
    
    def test_result_page_with_one_file_and_two_sequences(self):
        resultPage = self.client.post( '/align/result/', 
                                     {'fileA':open('./align/seqtest1.txt','r'),
                                      'sequenceA':'>1\nTTAGG',
                                      'sequenceB':'>2\nTTAGG'} )
        result_alignment = resultPage.context['result_alignment']

        self.assertEqual(result_alignment, "Error: You need to submit exactly 2 sequences")



