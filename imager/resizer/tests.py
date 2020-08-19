from django.test import TestCase
from resizer.forms import PhotoForm,PhotoDetalsForm
from resizer.models import Foto

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile



class NewPhotoTest(TestCase):

	def test_upload_file(self):
		form_data = {'photo':'test.jpg','image_url':None}
		form = PhotoForm(data=form_data,files={'photo':get_test_file()})
		self.assertTrue(form.is_valid())
	
	def test_url(self):
		url_dct = {'image_url':"https://test.com/test.jpg"}
		form = PhotoForm(url_dct,)
		self.assertTrue(form.is_valid())
	
	def test_both_none(self):
		form_data = {'photo':None,'image_url':None}
		form = PhotoForm(data=form_data)
		self.assertFalse(form.is_valid())
	
	def test_both_not_none(self):
		file_dict = {'photo': get_test_file()}
		url_dct = {'image_url':"https://test.com/test.jpg"}		
		form = PhotoForm(file_dict,url_dct)
		self.assertFalse(form.is_valid())


def get_test_file():
	im = Image.new(mode='RGB', size=(100, 100))
	im_io = BytesIO()
	im.save(im_io, 'JPEG')
	im_io.seek(0)
	return InMemoryUploadedFile(im_io, None, 'test.jpg', 'image/jpeg', len(im_io.getvalue()), None)
