from django.http import HttpResponse
from django.shortcuts import redirect, render
from webapp.forms import UserImageForm
from webapp.models import UploadImage

def home(request):
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_object = form.instance
            return render(request, 'home.html', {'form': form, 'img_obj': img_object})
    else:
        form = UserImageForm()

    return render(request, 'home.html', {'form': form})
