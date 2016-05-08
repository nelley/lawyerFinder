from django import forms
from lawyerFinder.models import Lawyer, LitigationType, Barassociation
from django.forms.extras.widgets import *

class LawyerForm(forms.ModelForm):
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
        
