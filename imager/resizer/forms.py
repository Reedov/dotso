#forms.py


from django import forms
from .models import Foto

class PhotoForm(forms.ModelForm):
    photo = forms.ImageField(label="Добавить изображение",required=False)
    image_url = forms.URLField(label="Добавить URL",required=False)
    class Meta:

        model = Foto
        fields = ('photo','image_url')

    def clean(self):
        super(PhotoForm, self).clean()
        photo = self.cleaned_data.get('photo')
        image_url = self.cleaned_data.get('image_url')
        
        if not photo and not image_url:
            self._errors['image_url'] = self.error_class(['Заполните одно поле']) 
        elif photo and image_url:
            self._errors['image_url'] = self.error_class(['Можно загрузить только один - локальный или по ссылке']) 
        
        if image_url and image_url[-4:] != ".jpg":
            self._errors['image_url'] = self.error_class(['ссылка на только на jpg'])
        elif photo and photo.__str__()[-4:] != ".jpg":
            self._errors['photo'] = self.error_class(['только jpg'])

        return self.cleaned_data 




class PhotoDetalsForm(forms.Form):
    length = forms.DecimalField(required=False, label="высота")
    width = forms.DecimalField(required=False, label="ширина")

    def clean(self):

        super(PhotoDetalsForm, self).clean()
        length = self.cleaned_data.get('length')
        width = self.cleaned_data.get('width')

        if not length and not width:
                self._errors['length'] = self.error_class(['Нужно ввести минимум 1 параметр']) 

        return self.cleaned_data 

