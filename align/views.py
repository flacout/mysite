from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse


from DNA_sequence import *
import global_align as al


from .models import Alignment


def index(request):
    return render(request, 'align/index.html', {'username': request.user.username})


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
        result_alignment=al.Alignment(sequenceA,sequenceB)
        name_alignment=fastSequenceA.name+"/"+fastSequenceB.name
    elif sequenceA=="" and sequenceB=="": 
        result_alignment=al.Alignment(fileA,fileB)
        name_alignment=fastFileA.name+"/"+fastFileB.name
    elif sequenceA=="" and fileB=="": 
        result_alignment=al.Alignment(fileA,sequenceB)
        name_alignment=fastFileA.name+"/"+fastSequenceB.name
    elif sequenceB=="" and fileA=="": 
        result_alignment=al.Alignment(sequenceA,fileB)
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


''' Page for the display of all the alignment results save in a user profile
    it display the entries from recent to old.
    you reach it from the navigation panel or after saving an alignment in 
    It contain a search button to search in the alignment_names.
'''
def allresults(request, page_nb=1):
    
    name = request.POST.get('name_align', 0)
    search= request.POST.get('search', 0)
    page_nb=int(page_nb)

    # Check if it comes from the align:result page
    if name!=0:
        # check if the result already exist.
        # If yes it display a text and don't save it.
        exist=Alignment.objects.filter(alignment_name=request.POST['name_align'])
        if len(exist)!=0:
            name_exist="the name of this alignment result already exist, it cannot be saved"
            alignments=Alignment.objects.filter(user_id=request.user.id).order_by('-id')
            alignments=alignments[(5*page_nb-5):(5*page_nb)]
            context={'alignments':alignments, 'username': request.user.username, 
                    'name_exist':name_exist, 'page_nb':page_nb}
            return render(request, 'align/allresults.html',context)

        # Create a new entry in the alignments of the user
        Alignment.objects.create(alignment_name=request.POST['name_align'],
                                alignment_result=request.POST['result_align'], user_id=request.user.id)
        alignments=Alignment.objects.filter(user_id=request.user.id).order_by('-id')
        alignments=alignments[(5*page_nb-5):(5*page_nb)]
        context={'alignments':alignments, 'username': request.user.username, 'page_nb':page_nb}
        return render(request, 'align/allresults.html',context)

    # Check if it comes from the search button
    if search!=0:
        alignments=Alignment.objects.filter(user_id=request.user.id).filter(
                            alignment_name__contains=request.POST['search']).order_by('-id')
        alignments=alignments[(5*page_nb-5):(5*page_nb)]

        # Chek if the search as a match or not
        if len(alignments)==0: 
            context={'alignments':alignments, 'username': request.user.username
                    ,'no_match': "No match for your search", 'page_nb':page_nb}
        else : context={'alignments':alignments, 'username': request.user.username, 'page_nb':page_nb}
        return render(request, 'align/allresults.html',context)

    # If it comes from the navigation menu
    else:
        alignments=Alignment.objects.filter(user_id=request.user.id).order_by('-id')
        alignments=alignments[(5*page_nb-5):(5*page_nb)]
        context={'alignments':alignments, 'username': request.user.username, 'page_nb':page_nb}
        return render(request, 'align/allresults.html',context)
