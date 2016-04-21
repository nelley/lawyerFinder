# coding: utf-8

from django.db import models
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import User


# group
class Barassociation(models.Model):
    AREAS = (
        ('TAIPEI', '台北'),
        ('TAICHUNG', '台中'),
        ('KAOHSIUNG', '高雄'),
        ('NANTOU', '南投'),
    )
    
    area = models.CharField(max_length=20, choices=AREAS)
    members = models.ManyToManyField('Lawyer', through='LawyerMembership',
                                     blank=False, 
                                     help_text=_('the area that lawyer have been registered in'), 
                                     verbose_name=_('Registered Area'))

# person
class Lawyer(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    lawyerId = models.CharField(max_length=32, blank=False)


# membership
class LawyerMembership(models.Model):
    lawyerId = models.ForeignKey(Lawyer)
    barAssociation = models.ForeignKey(Barassociation) 
    #date_joined = models.DateField()
    
