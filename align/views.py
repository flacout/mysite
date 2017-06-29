from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings

# import of custom modules
from align.DNA_sequence import FastaDNA
import align.global_align as ga

#import of databade models
from .models import Alignment


#---------------------------------------------------------------------------------------------
# Display the home page of the Alignment application, from where an
# alignment can be executed.
#---------------------------------------------------------------------------------------------
def index(request):
    return render(request, 'align/index.html', {'username': request.user.username})


#---------------------------------------------------------------------------------------------
# Display theresult page after execution of an alignment.
#---------------------------------------------------------------------------------------------
def result(request):
    sequenceA = tryGetSequence(request, 'sequenceA')
    sequenceB = tryGetSequence(request, 'sequenceB')
    fileA = tryGetFile(request, 'fileA')
    fileB = tryGetFile(request, 'fileB')
    sequences = makeSequenceList(sequenceA, fileA, sequenceB, fileB)

    if len(sequences) !=2: 
        name_alignment = ""
        result_alignment = "Error: You need to submit exactly 2 sequences"
    else :
        name_alignment = sequences[0].name+"/"+sequences[1].name
        result_alignment = ga.makeAlignment(sequences[0].sequence, sequences[1].sequence)

    saveResultToFile(name_alignment, result_alignment)
    context = {'result_alignment': result_alignment ,
               'name_alignment':name_alignment, 
               'username': request.user.username}
    return render(request, 'align/result.html', context)


def tryGetSequence(request, POSTSequence):
    try: return FastaDNA(request.POST[POSTSequence])
    except: return None


def tryGetFile(request, POSTFile):
    try: return FastaDNA(request.FILES[POSTFile].read().decode('UTF-8'))
    except: return None


def makeSequenceList(sequenceA, fileA, sequenceB, fileB):
    sequences = [sequenceA, fileA, sequenceB, fileB]
    i=0
    while i<len(sequences):
        if sequences[i]==None : 
            sequences.remove(sequences[i])
            i-=1
        i+=1
    return sequences


def saveResultToFile(name_alignment, result_alignment):
    filePath = settings.BASE_DIR+"/media/result.txt"
    text_file=open(filePath,'w')
    #Path on the web:
    #text_file=open("/home/fabricelacout/mysite/media/result.txt",'w')
    text_file.write(name_alignment+'\n'+result_alignment)
    text_file.close()


#---------------------------------------------------------------------------------------------
# Display a profile page that contain al alignment saved by the user
#---------------------------------------------------------------------------------------------
def accountResults(request, page_nb=1): 
    name = request.POST.get('name_align', 0)
    search = request.POST.get('search', '')
    change_page_button = request.POST.get('change_page', 0)
    deleteCheckbox = request.POST.getlist('alignmentCheckbox')
    page_nb=int(page_nb)
    if change_page_button !=0 : page_nb=int(change_page_button)


    # if it comes from the align:result page to save a record
    if name!=0: return saveRecord(request, name, page_nb)
    # Check if it comes from the search button
    elif len(search)!=0: return searchResult(request, search, page_nb)
    # if it come from delete button
    elif (deleteCheckbox): 
        for i in deleteCheckbox: Alignment.objects.filter(id=int(i)).delete()
        return showAllAlignmentsFiveByFive(request, page_nb)
    # if it comes from the navigation menu or next button
    else: return showAllAlignmentsFiveByFive(request, page_nb)


def saveRecord(request, name, page_nb):
    alignmentExist=Alignment.objects.filter(alignment_name=name)
    if (alignmentExist): return errorAlignmentAlreadyExist(request)
    else: return createNewRecordAndDisplay(request, page_nb)


def errorAlignmentAlreadyExist(request):
    errorStringAlignAlreadyExist='''the name of this alignment result already exist, 
                                    it cannot be saved'''
    context={'alignments':None, 
             'username': request.user.username, 
             'errorStringAlignAlreadyExist':errorStringAlignAlreadyExist,
             'page':1}
    return render(request, 'align/allresults.html',context)


def createNewRecordAndDisplay(request, page_nb):
    Alignment.objects.create(alignment_name=request.POST['name_align'],
                             alignment_result=request.POST['result_align'], 
                             user_id=request.user.id)
    return showAllAlignmentsFiveByFive(request, page_nb)
    

def showAllAlignmentsFiveByFive(request, page_nb):
    alignments = Alignment.objects.filter(user_id=request.user.id).order_by('-id')
    nb_entries = len(alignments)
    total_nb_pages = int(nb_entries/5)
    if (total_nb_pages*5) != nb_entries : total_nb_pages+=1

    alignments = alignments[(5*page_nb-5) : (5*page_nb)]
    context = {'alignments':alignments, 
               'username': request.user.username, 
               'page':page_nb, 
               'total_nb_pages':total_nb_pages}
    return render(request, 'align/allresults.html',context)


def searchResult(request, search,  page_nb):
    alignments=Alignment.objects.filter(user_id=request.user.id).filter(
                        alignment_name__contains=search).order_by('-id')
    # Chek if the search as a match or not
    if len(alignments)==0: context={'alignments':None, 
                                    'username': request.user.username,
                                    'no_match': "No match for your search", 
                                    'page':1, 'total_nb_pages':1}
    else : context={'alignments':alignments,
                    'username': request.user.username, 
                    'page':1, 'total_nb_pages':1}
    return render(request, 'align/allresults.html',context)