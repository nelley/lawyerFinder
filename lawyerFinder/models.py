# coding: utf-8
'''
from django.db import models
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator























#override default table
class AuthGroup(models.Model):

    ORDINARYUSER = 1
    LAWYER       = 2
    STUFF        = 3

    #parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(unique=True, max_length=80)
    is_expire = models.IntegerField()
    expire_function = models.CharField(max_length=32, blank=True, null=True)
    is_active = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        #managed = True
        db_table = 'auth_group'
        

#override default table
class User(AbstractUser):
    identifier = models.EmailField(max_length=254, unique=True, verbose_name=_('Email'))
    
    firstname = models.CharField(max_length=20, blank=False)
    lastname = models.CharField(max_length=20, blank=False)
    phone_number = models.CharField(max_length=20, blank=True)
    sendmail_failed_cnt = models.PositiveIntegerField(default=0)
    work_year = models.IntegerField(
                    default=1, 
                    validators=[
                        MaxValueValidator(80),
                        MinValueValidator(1)
                    ],
                    blank=True)
    auth_groups = models.ManyToManyField('AuthGroup', through='AuthUserGroups',blank=True, help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'), verbose_name=_('Member kind'))

    USERNAME_FIELD = 'identifier'
    class Meta:
        #managed = True
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    user = models.ForeignKey(User)
    groups = models.ForeignKey(AuthGroup)

    class Meta:
        #managed = True
        db_table = 'auth_user_groups'


-----------------------------------------------------------
class Specialty_field(models.Model):
    field = models.CharField(max_length=20, blank=False)
    percentage = models.IntegerField(
                    default=0, 
                    validators=[
                        MaxValueValidator(100),
                        MinValueValidator(0)
                    ],
                    blank=True)
    
    class Meta:
        managed = False
        db_table = 'lawyer_specialty_field'
        
# 3 group. admin, lawyer, user 
class User(AbstractUser):
    identifier = models.EmailField(max_length=254, unique=True, verbose_name=_('Email'))
    
    firstname = models.CharField(max_length=20, blank=False)
    lastname = models.CharField(max_length=20, blank=False)
    phone_number = models.CharField(max_length=20, blank=True)
    work_year = models.IntegerField(
                    default=1, 
                    validators=[
                        MaxValueValidator(80),
                        MinValueValidator(1)
                    ],
                    blank=True)
    specialty_fields = models.ManyToManyField(Specialty_field)
    #register_area = models.

    USERNAME_FIELD = 'identifier'
    
    class Meta:
        managed = False
        db_table = 'auth_user'
        
'''