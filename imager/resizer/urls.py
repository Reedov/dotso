from django.urls import path
from resizer.views import GetPhotoList,NewPhoto,PhotoDetail

urlpatterns = [
			path('',GetPhotoList,name='photo_list'),
			path('newphoto/', NewPhoto, name='newphoto'),
			path('photo_detail/', PhotoDetail, name='photo_detail'),
			path('photo_detail/<photo_id>', PhotoDetail, name='photo_detail'),

				]