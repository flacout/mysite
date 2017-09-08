from django.shortcuts import render
import re
import base64


#---------------------------------------------------------------------------------------------
# Display the home page of the Machine Learning application.
#---------------------------------------------------------------------------------------------

def index(request):

    if request.method== 'POST':
        imgstr = request.POST['canvasData']
        imgstr = re.search(r'base64,(.*)', imgstr).group(1)
        imgstr = base64.b64decode(imgstr)

        output = open('media/ml_number.png', 'wb')
        output.write(imgstr)
        output.close()
        return render(request, 'ml/index.html', {'username': request.user.username})
    else :
        return render(request, 'ml/index.html', {'username': request.user.username})
