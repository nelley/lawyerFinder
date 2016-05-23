from django import forms
from lawyerFinder.models import User
from django.forms.extras.widgets import *
from lawyerFinder.settings import *
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import logger
from PIL import Image
from django.utils.translation import ugettext_lazy as _
import re
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class User_reg_form(forms.ModelForm):
    
    CHOICES=[('YES','Yes'),
             ('NO','No')]
    
    
    username = forms.EmailField(label = _('username'), 
                                widget=forms.TextInput(attrs={'placeholder': 'newuser@mail.com'}),
                                required = False,
                                error_messages ={'invalid':_('Enter a valid email address')})
    password = forms.CharField(label = _('password'), 
                               widget=forms.PasswordInput,
                               required = False)
    checkpassword = forms.CharField(label = _('double check password'), 
                                    widget=forms.PasswordInput,
                                    required = False)
    
    siterule = forms.ChoiceField(choices=CHOICES, 
                                 widget=forms.RadioSelect(), label=_('agreements for site service policy'),
                                 required = False)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'checkpassword', 'siterule']
        
    def clean(self):
        
        cleaned_data = self.cleaned_data # individual field's clean methods have already been called
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("checkpassword")

        # check whether the user has been registered

        if password1 != password2:
            raise forms.ValidationError(_("Passwords does not identical."))

        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data['username'] # individual field's clean methods have already been called
        if (not username) or username is None:
            raise forms.ValidationError(_("Please input something."))
        
        return username
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if (not password) or password is None:
            raise forms.ValidationError(_("Please input something."))
        
        return password
        
    def clean_checkpassword(self):
        checkpassword = self.cleaned_data['checkpassword']
        if (not checkpassword) or checkpassword is None:
            raise forms.ValidationError(_("Please input something."))
        
        return checkpassword
    
    def clean_siterule(self):
        siterule = self.cleaned_data['siterule']
        if (not siterule) or siterule is None:
            raise forms.ValidationError(_("Please input something."))
        
        return siterule