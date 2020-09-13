from django.db import models

from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File


class Foto(models.Model):
    #photo_name = models.CharField(max_length=50,blank=False)
    photo = models.ImageField(blank=True,upload_to='')
    image_url = models.URLField(max_length=200,blank=True, default='http://')
    
    def __str__(self):
        return f"{self.photo}"

    def save(self): 
        if self.image_url and not self.photo:
            try:
                urlimage = urlopen(self.image_url).read()
            except Exception as e:
                print (e)
                return

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlimage)
            img_name = self.image_url.split("/")[-1]
            img_temp.flush()
            self.photo.save(f"url_{img_name}", File(img_temp))
            
        super(Foto, self).save()
