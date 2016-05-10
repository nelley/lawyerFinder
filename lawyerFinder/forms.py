from django import forms
from lawyerFinder.models import Lawyer, LitigationType, Barassociation
from django.forms.extras.widgets import *
from lawyerFinder.settings import *
from django.core.exceptions import ValidationError
from PIL import Image
import re

class Lawyer_SearchForm(forms.ModelForm):
    gender = forms.MultipleChoiceField(required=True, 
                                       choices=Lawyer.GENDER,
                                       )
    class Meta:
        model = Lawyer
        fields = ['gender']
        #fields = '__all__'
        
class LitigationTypeForm(forms.ModelForm):
    category =  forms.MultipleChoiceField(required=True, 
                                          choices=LitigationType.CATEGORYS,
                                          # add attr to HTML
                                          #widget=formsSelectMultiple(attrs={'title':'test'})
                                          )
    class Meta:
        model = LitigationType
        fields = ['category']

        
class BarassociationForm(forms.ModelForm):
    area = forms.MultipleChoiceField(required=True, 
                                          choices=Barassociation.AREAS,
                                          # add attr to HTML
                                          #widget=formsSelectMultiple(attrs={'title':'test'})
                                          )
    class Meta:
        model = Barassociation
        fields = ['area']
        
        
class Lawyer_RegForm(forms.ModelForm):
    PROFILE_IMAGE_WIDTH = 120
    PROFILE_IMAGE_HEIGHT = 120
    class Meta:
        model = Lawyer
        #fields = ['lawyerNo', 'gender', 
        #          'careerYear', 'companyAddress', 
        #          'regBarAss', 'specialty', 'photos']
        fields = ['photos']
        
    def clean_photos(self):
        photo = self.cleaned_data.get('photos', False)
        if photo:
            # validation for file type
            format = Image.open(image.file).format
            image.file.seek(0)
            if format not in MEDIA_BANNER_IMAGE_VALID_FILETYPES:
                raise ValidationError(_("file type doesn't permit."))

            # validation for file size
            if image.size > MEDIA_BANNER_IMAGE_MAX_UPLOAD_SIZE:
                raise ValidationError(_("Image file too large."))
        return photo

    def save(self, commit=True):
        super(LawyerForm, self).save(commit)

        if self.instance.image:
            print(self.instance.image.path)
            self._resize_image(self.instance.image.path)

    def _resize_image(self, image_path):
        image = Image.open(image_path)
        width, height = image.size

        if width > height:
            aspect_ratio = MEDIA_BANNER_IMAGE_WIDTH / float(width)
        else:
            aspect_ratio = MEDIA_BANNER_IMAGE_HEIGHT / float(height)

        adjusted_width = int(width * aspect_ratio)
        adjusted_height = int(height * aspect_ratio)
        image = image.resize((adjusted_width, adjusted_height), Image.ANTIALIAS)
        image.save(image_path)
