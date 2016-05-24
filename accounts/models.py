from django.db import models
# Create your models here.
# --- coding: utf-8 ---

import re
from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, _user_has_perm
)
from django.contrib.auth.models import Group, User, PermissionsMixin
from django.core import validators
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.handlers.wsgi import logger

class UserManager(BaseUserManager):
    def create_user(self, username, email, password, active_flag, **extra_fields):
        """ Creates and saves User with the given email and password. """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address.')
        email = UserManager.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_active=active_flag,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        logger.debug('superuser creation start!')
        """ Creates and saves a superuser with the given email and password. """
        user = self.create_user(username, email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User """
    username    = models.EmailField(_('username'),
                                   max_length=100,
                                   unique=True,
                                   help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                                   '@/./+/-/_ characters'),
                                   blank=False)
    first_name  = models.CharField(_('first name'), max_length=30, blank=True)
    last_name   = models.CharField(_('last name'), max_length=30, blank=True)
    email       = models.EmailField(verbose_name='email address', max_length=100, unique=True, blank=True)
    is_active   = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    is_admin    = models.BooleanField(default=False)
    premiumUser = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    loginCnt    = models.PositiveIntegerField(default=0)
    
    objects = UserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

    def email_user(self, subject, message, from_email=None):
        """Send an email to this User. """
        send_mail(subject, message, from_email, [self.email])

    def user_has_perm(user, perm, obj):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        return _user_has_perm(user, perm, obj)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name
    
    
    # NL defined
    #def __unicode__(self):
    #l    return self.email
    
    '''
class AuthGroup(models.Model):
    ORDINARYUSER = 1
    LAWYER       = 2
    
    STAFF        = 3
    WRITER       = 4
    VIEWER       = 5
    MANAGER      = 6
    
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(unique=True, max_length=80)
    is_expire = models.PositiveIntegerField()
    expire_function = models.CharField(max_length=32, blank=True, null=True)
    auth_groups = models.ManyToManyField('User', through='Membership', blank=True, 
                                     help_text=_('The groups which user belongs to.'), 
                                     verbose_name=_('Member kind'))
    
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'auth_group'

# joint table
class Membership(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
'''
    
    
    
    