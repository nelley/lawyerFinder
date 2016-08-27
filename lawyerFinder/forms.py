# -*- coding: utf-8 -*-
from django import forms
from lawyerFinder.models import *
from django.forms.extras.widgets import *
from lawyerFinder.settings import *
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import logger
from PIL import Image
from django.utils.translation import ugettext_lazy as _
import re
from django.utils.safestring import mark_safe
from accounts.forms import User_reg_form
from django.contrib.contenttypes import fields
from ckeditor.widgets import CKEditorWidget
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.forms import Widget


class Lawyer_infosForm(forms.ModelForm):
    # used for all fields(strongfield, finishedCases.....)
    basic = forms.CharField(widget=CKEditorWidget(config_name='default'),
                              label='')
    class Meta:
        model = Lawyer_infos
        fields = ['basic']
        #fields = '__all__'


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

class HorizontalCheckBoxRenderer(forms.CheckboxSelectMultiple.renderer):
    def render(self):
        tmp = mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
        tmp = '<br>' + tmp
        return tmp
        #return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
    
class PartialSelectedCheckBox(forms.CheckboxSelectMultiple):
    """Renders custom regBarAss/specialty into an html string
    
    """
    
    def __init__(self, *args, **kwargs):
        if 'userobj' in kwargs:
            self.userobj = kwargs.pop('userobj')
        if 'value' in kwargs:#strong field | registered area
            self.value = kwargs.pop('value')
            
        super(PartialSelectedCheckBox, self).__init__(*args, **kwargs)
        
        
    def render(self, name, value, attrs=None):
        
        id_ = self.attrs.get('id', None)
        start_tag = format_html('<div id="{0}">', id_) if id_ else '<div>'
        output = [start_tag]
        iterate_items = ''
        
        if name=='regBarAss':
            #convert queryset to list
            iterate_items = self.userobj.regBarAss.all().values_list('area',flat=True)
        else:
            #get the No of category, and convert to list
            matchField = LitigationType.objects.all()
            litigationtype_id = self.userobj.lawyerspecialty_set.filter(litigations=matchField).values_list('litigations',flat=True)
            iterate_items = LitigationType.objects.filter(id__in=litigationtype_id).values_list('category',flat=True)
            
        #print iterate_items
        for i, val in enumerate(self.value):
            if val[0] in iterate_items:
                output.append(format_html(u'<label for="id_{0}_{1}"><input class="" id="id_{0}_{1}" name="{0}" checked="checked" title="可複選" type="checkbox" value="{2}" /> {3}</label>',
                                          id_, i, val[0], val[1]))
            else:
                output.append(format_html(u'<label for="id_{0}_{1}"><input class="" id="id_{0}_{1}" name="{0}" title="可複選" type="checkbox" value="{2}" /> {3}</label>',
                                          id_, i, val[0], val[1]))
        output.append(u'</div>')
        return mark_safe('\n'.join(output))
        
        
class Lawyer_photoForm(forms.ModelForm):
    photos = forms.ImageField(required=False, label=_('Profile Photo'))
    
    class Meta:
        model = Lawyer
        fields = ['photos']
        
    
    def clean_photos(self):
        logger.debug('clean photos starts')
        try:
            print 'photo first'
            photo = self.cleaned_data.get('photos', False)
            print photo

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
                raise ValidationError(e)
                
        except Exception as e:
            raise ValidationError(e)
        
        logger.debug('clean photos end')
        return photo
    
    
    
    #def save(self, commit=True):
        #print 'save photos start'
        #super(LawyerForm, self).save(commit)


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

    
class Lawyer_RegForm(forms.ModelForm):
    
    lawyerNo = forms.CharField(max_length=7, required=False, label=_('Certification Number'))
    careerYear = forms.IntegerField(required=False, label=_('Work Years'))
    companyAddress = forms.CharField(required=False, label=_('Company\'s Address'))
    phone_number = forms.CharField(max_length=20, required=False)
    gender = forms.ChoiceField(choices=Lawyer.GENDER, required=True, label=_('gender'))
    regBarAss = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(renderer=HorizontalCheckBoxRenderer),
                                                 choices=Barassociation.AREAS,
                                                 label=_('Registered Area'),
                                                 help_text=_('multi-selection is permitted'),
                                                 required=True)
    
    specialty = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(renderer=HorizontalCheckBoxRenderer),
                                                 choices=LitigationType.CATEGORYS,
                                                 label=_('Strong Field'),
                                                 help_text=_('multi-selection is permitted'),
                                                 required=True)
    
    class Meta:
        model = Lawyer
        fields = ['lawyerNo', 'gender', 
                  'careerYear', 'companyAddress', 'phone_number',
                  'regBarAss', 'specialty']
        
    def __init__(self, request, *args, **kwargs):
        #when calling in lawyer_home
        if 'lawyer' in kwargs:
            self.lawyer = kwargs.pop('lawyer')
            super(Lawyer_RegForm, self).__init__(*args, **kwargs)
            
            self.fields['regBarAss'] = forms.MultipleChoiceField(required=True,
                                                                 label=_('Registered Area'),
                                                                 help_text=_('multi-selection is permitted'),
                                                                 widget=PartialSelectedCheckBox(value=Barassociation.AREAS,
                                                                                                userobj=self.lawyer)
                                                                 )
            self.fields['specialty'] = forms.MultipleChoiceField(required=True,
                                                                 label=_('Strong Field'),
                                                                 help_text=_('multi-selection is permitted'),
                                                                 widget=PartialSelectedCheckBox(value=LitigationType.CATEGORYS,
                                                                                                userobj=self.lawyer)
                                                                 )
            
            
        else:
            self.request = request
            super(Lawyer_RegForm, self).__init__(*args, **kwargs)
        
    def save_custom(self):
        print 'Lawyer_RegForm saved!!'
        
    def clean_lawyerNo(self):
        tmpLawyerNo = self.cleaned_data['lawyerNo']
        if tmpLawyerNo and tmpLawyerNo is not None:
            if self.request.user.is_authenticated():
                session_Lawyer = Lawyer.objects.filter(user_id = self.request.session['_auth_user_id'])
                if session_Lawyer[0].lawyerNo == tmpLawyerNo:
                    logger.debug('lawyerNo is the same')
                    return tmpLawyerNo #
                else:
                    tmpLawyer = Lawyer.objects.filter(lawyerNo=tmpLawyerNo)
                    if tmpLawyer.count() > 0:
                        raise forms.ValidationError(_("This Lawyer Number has been registered"))
        else:
            raise forms.ValidationError(_("Please input something."))
        
        return tmpLawyerNo
    
    def clean_careerYear(self):
        careerYear = self.cleaned_data['careerYear']
        if careerYear is None :
            careerYear = 0
        elif careerYear < 0:
            raise forms.ValidationError(_("Please do not input minus number."))
        return careerYear
    
    def clean_regBarAss(self):
        regBarAss = self.cleaned_data['regBarAss']
        if (not regBarAss) or regBarAss is None:
            raise forms.ValidationError(_("Please at least choose one field."))
        
        return regBarAss
    
    def clean_specialty(self):
        specialty = self.cleaned_data['specialty']
        if (not specialty) or specialty is None:
            raise forms.ValidationError(_("Please at least choose one field."))
        
        return specialty
    
    