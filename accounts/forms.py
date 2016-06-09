from django import forms
from lawyerFinder.models import User
from django.forms.extras.widgets import *
from lawyerFinder.settings import *
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import logger
from PIL import Image
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
import re
from django.contrib.auth.hashers import make_password
from django.utils.safestring import mark_safe


# for temporary use
class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        tmp = mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
        tmp = '<br>' + tmp
        return tmp


class User_Loginform(forms.ModelForm):

    username = forms.EmailField(label = _('username'),
                                widget=forms.TextInput(attrs={'placeholder': 'Email Account'}),
                                required = False,
                                error_messages ={'invalid':_('Enter a valid email address')})
    password = forms.CharField(label=_('password'),
                               widget=forms.PasswordInput,
                               required = False)

    class Meta:
        model = User
        fields = ['username', 'password']
    
    def __init__(self, *args, **kwargs):
        super(User_Loginform, self).__init__(*args, **kwargs)
    
    def clean(self): #have to override, if not, User model's clean method will raise some eroor
        logger.debug('full clean')
        cleaned_data = self.cleaned_data # individual field's clean methods have already been called

        return cleaned_data
    
    def clean_username(self): # called first
        logger.debug('clean username!')
        username = self.cleaned_data['username'] # individual field's clean methods have already been called
        if (not username) or username is None:
            raise forms.ValidationError(_("Please input something."))
        return username
    
    def clean_password(self):
        logger.debug('clean password!')
        password = self.cleaned_data['password']
        if (not password) or password is None: #check empty or NONE
            raise forms.ValidationError(_("Please input something."))
            
        return password


class User_reg_form(User_Loginform):
    
    CHOICES=[('YES','Yes'),
             ('NO','No')]
    
    checkpassword = forms.CharField(label = _('double check password'), 
                                    widget=forms.PasswordInput,
                                    required = False)
    siterule = forms.ChoiceField(choices=CHOICES, 
                                 widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), 
                                 label=_('agreements for site service policy'),
                                 required = False)
    
    class Meta(User_Loginform.Meta):
        fields = ['username', 'password', 'checkpassword', 'siterule']
    
    def __init__(self, *args, **kwargs):
         super(User_reg_form, self).__init__(*args, **kwargs)
         #self.fields['siterule'].widget.attrs['label'] = 'test'
    
    def save_custom(self):
        print 'User_reg_form saved!!'
    
    def clean(self): #this will be called at the last
        logger.debug('pw checkpw confirmation')
        cleaned_data = self.cleaned_data # individual field's clean methods have already been called
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("checkpassword")

        #if the checks before all passed
        if (not self.errors):
            # password length check
            if len(password1) < 6:
               raise forms.ValidationError(_("Password should be longer than 6 digits"))

            # check whether the user has been registered
            if password1 != password2:
                print 'not same'
                del cleaned_data['password']
                del cleaned_data['checkpassword']
                raise forms.ValidationError(_("Passwords does not identical."))
        
        return cleaned_data
        
    
    def clean_username(self): # called first
        logger.debug('clean username!')
        username = self.cleaned_data['username'] # individual field's clean methods have already been called
        if username and username is not None:
            tmpUser = User.objects.filter(username=username)
            if tmpUser.count() > 0:
                raise forms.ValidationError(_("This ID has been registered."))
        else:
            raise forms.ValidationError(_("Please input something."))
        return username
    
    def clean_checkpassword(self):
        logger.debug('clean checkpassword!')
        checkpassword = self.cleaned_data['checkpassword']
        if (not checkpassword) or checkpassword is None:
            raise forms.ValidationError(_("Please input something."))
        
        return checkpassword
    
    def clean_siterule(self):
        logger.debug('clean siterule!')
        siterule = self.cleaned_data['siterule']
        if siterule or siterule is not None:
            if siterule == 'NO' or (not siterule):
                raise forms.ValidationError(_("Please agree before you register."))
        else:
            raise forms.ValidationError(_("Please input something."))
        
        return siterule
        