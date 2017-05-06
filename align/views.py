from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

# import of custom modules
from DNA_sequence import FastaDNA
import global_align as ga

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
    name_alignment=""
    result_alignment=""
    sequenceA=""
    sequenceB=""
    fileA=""
    fileB=""

    try: 
        fastSequenceA=FastaDNA(request.POST['sequenceA'])
        sequenceA = fastSequenceA.sequence
    except:pass
    try:
        fastSequenceB=FastaDNA(request.POST['sequenceB'])
        sequenceB = fastSequenceB.sequence
    except:pass
    try:
        fastFileA=FastaDNA(request.FILES['fileA'].read())
        fileA=fastFileA.sequence
    except:pass
    try: 
        fastFileB=FastaDNA(request.FILES['fileB'].read())
        fileB=fastFileB.sequence
    except:pass

    if sequenceA=="" and sequenceB=="" and (fileA=="" or fileB==""): 
        name_alignment=""
        result_alignment="You need to submit at least 2 sequences"
    elif fileA=="" and fileB=="": 
        result_alignment=ga.makeAlignment(sequenceA,sequenceB)
        name_alignment=fastSequenceA.name+"/"+fastSequenceB.name
    elif sequenceA=="" and sequenceB=="": 
        result_alignment=ga.makeAlignment(fileA,fileB)
        name_alignment=fastFileA.name+"/"+fastFileB.name
    elif sequenceA=="" and fileB=="": 
        result_alignment=ga.makeAlignment(fileA,sequenceB)
        name_alignment=fastFileA.name+"/"+fastSequenceB.name
    elif sequenceB=="" and fileA=="": 
        result_alignment=ga.makeAlignment(sequenceA,fileB)
        name_alignment=fastSequenceA.name+"/"+fastFileB.name
    else : 
        name_alignment=""
        result_alignment="Submit a file or paste a sequence, not both"

    #save result on a file for future download.
    text_file=open("./media/result.txt",'w')
    text_file.write(name_alignment+'\n'+result_alignment)
    text_file.close()

    context = {'result_alignment': result_alignment ,'name_alignment':name_alignment, 
                'username': request.user.username}
    return render(request, 'align/result.html', context)


#---------------------------------------------------------------------------------------------
# Display a profile page that contain al alignment saved by the user
#---------------------------------------------------------------------------------------------
def accountResults(request, page_nb=1):
    
    name = request.POST.get('name_align', 0)
    search= request.POST.get('search', '')
    change_page_button = request.POST.get('change_page', 0)
    deleteCheckbox = request.POST.getlist('alignmentCheckbox')

    page_nb=int(page_nb)
    alignments=Alignment.objects.filter(user_id=request.user.id).order_by('-id')
    nb_entries = len(alignments)
    total_nb_pages = int(nb_entries/5)
    if (total_nb_pages*5) != nb_entries : total_nb_pages+=1

    if change_page_button !=0 : page_nb=int(change_page_button)

    # Check if it comes from the align:result page
    if name!=0:
        # check if the result already exist.
        # If yes it display a text and don't save it.
        exist=Alignment.objects.filter(alignment_name=request.POST['name_align'])
        if len(exist)!=0:
            nameOfAlignAlreadyExist='''the name of this alignment result already exist, 
                                      it cannot be saved'''
            alignments=Alignment.objects.filter(user_id=request.user.id).order_by('-id')
            alignments=alignments[(5*page_nb-5):(5*page_nb)]
            context={'alignments':alignments, 'username': request.user.username, 
                    'nameOfAlignAlreadyExist':nameOfAlignAlreadyExist, 'page':page_nb}
            return render(request, 'align/allresults.html',context)

        # Create a new entry in the alignments of the user
        Alignment.objects.create(alignment_name=request.POST['name_align'],
                                alignment_result=request.POST['result_align'], 
                                user_id=request.user.id)
        alignments=Alignment.objects.filter(user_id=request.user.id).order_by('-id')
        alignments=alignments[(5*page_nb-5):(5*page_nb)]
        context={'alignments':alignments, 'username': request.user.username, 'page':page_nb}
        return render(request, 'align/allresults.html',context)

    # Check if it comes from the search button
    if len(search)!=0:
        alignments=Alignment.objects.filter(user_id=request.user.id).filter(
                            alignment_name__contains=request.POST['search']).order_by('-id')

        # Chek if the search as a match or not
        if len(alignments)==0: 
            context={'alignments':alignments, 'username': request.user.username
                    ,'no_match': "No match for your search", 'page':1, 'total_nb_pages':1}
        else : context={'alignments':alignments, 'username': request.user.username, 
                    'page':1, 'total_nb_pages':1}
        return render(request, 'align/allresults.html',context)


    # check if it come from delete button
    if (deleteCheckbox): 
        for i in deleteCheckbox: Alignment.objects.filter(id=int(i)).delete()
        return treatNormalDisplay(request, page_nb, total_nb_pages)


    # If it comes from the navigation menu
    else:
        alignments=Alignment.objects.filter(user_id=request.user.id).order_by('-id')
        alignments=alignments[(5*page_nb-5):(5*page_nb)]
        context={'alignments':alignments, 'username': request.user.username, 
                'page':page_nb, 'total_nb_pages':total_nb_pages}
        return render(request, 'align/allresults.html',context)

def treatNormalDisplay(request, page_nb, total_nb_pages):
        alignments=Alignment.objects.filter(user_id=request.user.id).order_by('-id')
        alignments=alignments[(5*page_nb-5):(5*page_nb)]
        context={'alignments':alignments, 'username': request.user.username, 
                'page':page_nb, 'total_nb_pages':total_nb_pages}
        return render(request, 'align/allresults.html',context)