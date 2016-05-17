from django import forms
from lawyerFinder.models import Lawyer, LitigationType, Barassociation
from django.forms.extras.widgets import *
from lawyerFinder.settings import *
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import logger
from PIL import Image
from django.utils.translation import ugettext_lazy as _
import re

class Lawyer_SearchForm(forms.ModelForm):
    gender = forms.MultipleChoiceField(required=True, 
                                       choices=Lawyer.GENDER,
                                       label=_('Gender')
                                       )
    class Meta:
        model = Lawyer
        fields = ['gender']
        #fields = '__all__'
        
class LitigationTypeForm(forms.ModelForm):
    category =  forms.MultipleChoiceField(required=True, 
                                          choices=LitigationType.CATEGORYS,
                                          label=_('Categorys')
                                          # add attr to HTML
                                          #widget=formsSelectMultiple(attrs={'title':'test'})
                                          )
    class Meta:
        model = LitigationType
        fields = ['category']


class BarassociationForm(forms.ModelForm):
    area = forms.MultipleChoiceField(required=True, 
                                     choices=Barassociation.AREAS,
                                     label=_('Areas')
                                     # add attr to HTML
                                     #widget=formsSelectMultiple(attrs={'title':'test'})
                                     )
    class Meta:
        model = Barassociation
        fields = ['area']

        
class Lawyer_RegForm(forms.ModelForm):
    PROFILE_IMAGE_WIDTH = 120
    PROFILE_IMAGE_HEIGHT = 120
    
    lawyerNo = forms.CharField(max_length=15, required=True,label=_('Certification Number'))
    careerYear = forms.IntegerField(required=False, label=_('Work Years'))
    companyAddress = forms.CharField(required=False, label=_('Company\'s Address'))
    photos = forms.ImageField(required=False, label=_('Profile Photo'))
    gender = forms.ChoiceField(choices=Lawyer.GENDER, required=True, label=_('gender'))
    regBarAss = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                 choices=Barassociation.AREAS,
                                                 label=_('Registered Area'),
                                                 help_text=_('multi-selection is permitted'),
                                                 required=True)
    
    specialty = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                 choices=LitigationType.CATEGORYS,
                                                 label=_('Strong Field'),
                                                 help_text=_('multi-selection is permitted'),
                                                 required=True)
    
    class Meta:
        model = Lawyer
        fields = ['lawyerNo', 'gender', 
                  'careerYear', 'companyAddress', 
                  'regBarAss', 'specialty', 'photos']
        #fields = ['photos']
        
        
    def clean_photos(self):
        logger.debug('clean photos starts')
        try:
            photo = self.cleaned_data.get('photos', False)

            if photo is not None:
                # validation for file type
                format = Image.open(photo.file).format
                photo.file.seek(0)
                
                if format not in MEDIA_BANNER_IMAGE_VALID_FILETYPES:
                    raise ValidationError("file type doesn't permit.")
            
                # validation for file size
                if photo.size > MEDIA_BANNER_IMAGE_MAX_UPLOAD_SIZE:
                    raise ValidationError("Image file too large.")
                
            else:
                # add logic to attach default image file
                print 'NONE TYPE'
                
        except Exception as e:
            raise ValidationError(e)
        
        logger.debug('clean photos end')
        return photo

    def save(self, commit=True):
        print 'save photos start'
        super(LawyerForm, self).save(commit)


        #if self.instance.image:
        #    print(self.instance.image.path)
        #    self._resize_image(self.instance.image.path)


    def _resize_image(self, image_path):
        image = Image.open(image_path)
        width, height = image.size

        if width > height:
            aspect_ratio = self.PROFILE_IMAGE_WIDTH / float(width)
        else:
            aspect_ratio = self.PROFILE_IMAGE_HEIGHT / float(height)

        adjusted_width = int(width * aspect_ratio)
        adjusted_height = int(height * aspect_ratio)
        image = image.resize((adjusted_width, adjusted_height), Image.ANTIALIAS)
        image.save(image_path)
