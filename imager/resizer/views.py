from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from django.core.exceptions import ValidationError


from .forms import PhotoForm,PhotoDetalsForm
from .models import Foto



def GetPhotoList(request):
    photos = Foto.objects.all()
    return render(request,'resizer/index.html',context = {'photos':photos})

def NewPhoto(request):

    if request.method == 'GET':
        """изначальная загрузка формы"""
        form = PhotoForm()
        return render(request, 'resizer/newphoto.html', context = {'form': form})

    elif request.method == 'POST':
        """обработка заполненой формы"""
        form = PhotoForm(request.POST,request.FILES)
        if form.is_valid():
            print ("form.cleaned_data['photo']",form.cleaned_data['photo'])
            
            newphoto = form.save()
            
            print (dir(newphoto))
            photo_id = newphoto.id
            if photo_id:
                return redirect('photo_detail',photo_id)
        
        return render(request, "resizer/newphoto.html", {'form': form})


def PhotoDetail(request,photo_id):

    photo = Foto.objects.get(id=photo_id)
    photo_name = photo.photo
    photo_url = photo.photo.url

    if request.method == 'GET':
        form = PhotoDetalsForm()
        return render(request, 'resizer/photo_detail.html', context = {'form':form,
                                                                        'photo_name':photo_name,
                                                                        'photo_url':photo_url})

    elif request.method == 'POST':        
        form = PhotoDetalsForm(request.POST)
        if form.is_valid():

            l= form.cleaned_data['length']
            w= form.cleaned_data['width']

            photo_url = photo_resize(photo,w,l)
        
            return render(request, 'resizer/photo_detail.html', context = {'form':form,
                                                                       'photo_name':photo_name,
                                                                       'photo_url':photo_url})
        else:
            return render(request, "resizer/photo_detail.html", {'form':form,
                                                                 'photo_name':photo_name,
                                                                 'photo_url':photo_url})


def photo_resize(photo,l=None,w=None):
    print (l,w)
    file_buffer = BytesIO()
    im = Image.open(photo.photo)
    image_length,image_width = im.size
    ratio = image_width/image_length
    if not l:
        l = round(int(w)/ratio)
    elif not w:
        w = round(int(l)*ratio)

    print (l,w)
    photo_instance = Foto()

    resized_photo = im.resize((l,w),Image.ANTIALIAS)
    resized_photo.save(file_buffer, 'JPEG')


    photo_string = photo.__str__()
    photo_name = f"{photo_string.split('.')[0]}_{l}x{w}.jpg"

    resized_photo = ContentFile(file_buffer.getvalue(), photo_name)

    photo_instance.photo = resized_photo
    photo_instance.save()


    return photo_instance.photo.url


