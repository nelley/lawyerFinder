# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import User
from django.db.models.fields.related import RelatedField
import datetime
from django.utils import timezone
from django.db import connection
from random import randint
from ckeditor.fields import RichTextField

import sys

class LawyerSpecialtyManager(models.Manager):
    def create_in_bulk(self, target, obs):
        base_sql = "INSERT INTO lawyerfinder_lawyerspecialty (lawyerNo_id, litigations_id, caseNum) VALUES (%s, %s, %s) "
        
        values_data = []
        for value in obs:
            num = randint(0,100) # num is caseNum
            tmpTuple = (target.user_id, value.id, num)
            values_data.append(tmpTuple)
            
        curs = connection.cursor()
        curs.executemany(base_sql, values_data)
        
class LawyerMembershipManager(models.Manager):
    def create_in_bulk(self, target, obs):
        base_sql = "INSERT INTO lawyerfinder_lawyermembership (lawyerNo_id, barAssociation_id, date_joined) VALUES (%s, %s, %s) "
        now = timezone.now().strftime("%Y-%m-%d")
        
        values_data = []
        for value in obs:
            tmpTuple = (target.user_id, value.id, now)
            values_data.append(tmpTuple)
            
        curs = connection.cursor()
        curs.executemany(base_sql, values_data)
# group
class Barassociation(models.Model):
    # tuple
    AREAS = (
        ('KEELUNG', '基隆'),
        ('TAIPEI', '台北'),
        ('HSINCHU', '新竹'),
        ('TAICHUNG', '台中'),
        ('TAINAN', '台南'),
        ('YILAN', '宜蘭'),
        ('TAOYUAN', '桃園'),
        ('MIAOLI', '苗栗'),
        ('CHANGHUS', '彰化'),
        ('YUNLIN', '雲林'),
        ('CHIAYI', '嘉義'),
        ('PINGTUNG', '屏東'),
        ('TAITUNG', '台東'),
        ('HUALIEN', '花蓮'),
        ('PENGHU', '澎湖'),
        ('KAOHSIUNG', '高雄'),
        ('NANTOU', '南投'),
    )
    area = models.CharField(max_length=20, choices=AREAS, 
                            verbose_name=_('AREA:'),
                            help_text=_('Please Choose The Area'))

    area_cn = models.CharField(max_length=20, choices=AREAS)



# person
class Lawyer(models.Model): 
    GENDER = (
        ('M', '男性'),
        ('F', '女性'),
    )
    
    PREMIUM = (
        ('1', '普通會員'), #STD
        ('2', '黃金會員'), #GOLDEN
        ('3', '白金會員'), #PLATINUM
        ('4', '鑽石會員'), #DIAMOND
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='foobar')
    lawyerNo = models.CharField(max_length=32, blank=True, help_text=_('please input the lawyer certification number '))
    premiumType = models.CharField(max_length=30, blank=True, default='1')
    gender = models.CharField(max_length=20, choices=GENDER, blank=True)
    careerYear = models.IntegerField(null=True, blank=True, default=0, help_text=_('please input the career year'))
    companyAddress = models.CharField(max_length=50, blank=True, help_text=_('please input the company\'s address'))
    regBarAss = models.ManyToManyField('Barassociation', through='LawyerMembership',
                                     blank=True, 
                                     help_text=_('the area that lawyer have been registered in'), 
                                     verbose_name=_('Registered Bar Association'))
    
    specialty = models.ManyToManyField('LitigationType', through='LawyerSpecialty',
                                     blank=True, 
                                     help_text=_('the strong field of this lawyer'), 
                                     verbose_name=_('the strong field of this lawyer'))
    phone_regex = RegexValidator(regex=r'\d{2,4}\-\d{3,5}\-\d{3,5}$',
                                    message=_("Phone number must be entered in the format xxxx-xxx-xxx or xx-xxxx-xxxx"))
    phoneNumber = models.CharField(max_length=20, validators=[phone_regex], blank=True)
    thumbnail = models.ImageField(u'thumbnail', max_length=255, blank=True)
    photos = models.ImageField(u'image', upload_to='/home/nelley/Downloads/', max_length=255, blank=True)

    def __str__(self):
        matchField = LitigationType.objects.all()
        #reload(sys)
        #sys.setdefaultencoding('UTF8')
        # return JSON formatted string
        return "{\"first_name\":\"%s\",\"careerYear\":\"%s\",\"gender\":\"%s\",\"premiumType\":\"%s\",\"lawyerNo\":\"%s\",\"area\":[%s],\"caseNum\":[%s]}" % (
                                      self.user.first_name,
                                      self.careerYear,
                                      self.gender, 
                                      self.premiumType,
                                      self.lawyerNo,
                                      ",".join('\"'+bar.area_cn+'\"' for bar in self.regBarAss.all()), 
                                      ",".join(('{\"'+field.litigations.category_cn + '\":\"' + str(field.caseNum)+ '\"}')
                                                for field in self.lawyerspecialty_set.filter(litigations=matchField))
                                      )

    def print_json(self):
        matchField = LitigationType.objects.all()
        return "{\"first_name\":\"%s\",\"careerYear\":\"%s\",\"gender\":\"%s\",\"premiumType\":\"%s\",\"lawyerNo\":\"%s\",\"area\":[%s],\"strongField\":[%s]}" % (
                                      self.user.first_name,
                                      self.careerYear,
                                      self.gender, 
                                      self.premiumType,
                                      self.lawyerNo,
                                      ",".join('\"'+bar.area+'\"' for bar in self.regBarAss.all()), 
                                      ",".join(('\"'+field.litigations.category+'\"')
                                                for field in self.lawyerspecialty_set.filter(litigations=matchField))
                                      )

class Lawyer_infos(models.Model):
    lawyer = models.OneToOneField(Lawyer, on_delete=models.CASCADE, 
                                  primary_key=True, related_name='lawyer_info',
                                  )
    basic = RichTextField(max_length=130, blank=True)
    strongFields = RichTextField(max_length=130, blank=True)
    finishedCases = RichTextField(max_length=130, blank=True)
    feeStd = RichTextField(max_length=130, blank=True)
    companyInfos = RichTextField(max_length=130, blank=True)


# membership
class LawyerMembership(models.Model):
    lawyerNo = models.ForeignKey(Lawyer)
    barAssociation = models.ForeignKey(Barassociation) 
    date_joined = models.DateField(null=True, default=datetime.date.today)
    
    # custom manager
    objects = LawyerMembershipManager()
#---------------------------------------------------------------
class LitigationType(models.Model):
    CATEGORYS = (
        ('EC', '感情事件'), ('IP', '智慧財產'), ('MD', '醫療糾紛'), ('IW', '網路世界'), ('EP', '毒品問題'),
        ('PC', '支付命令'), ('GP', '政府採購'), ('PE', '環境保護'), ('FC', '詐騙案件'), ('HI', '遺產繼承'),
        ('CI', '公司經營'), ('CD', '車禍糾紛'), ('ID', '保險爭議'), ('RD', '營造工程'), ('BC', '兒少事件'),
        ('SA', '性侵案件'), ('LA', '訴訟程序'), ('LP', '勞資糾紛'), ('BD', '銀行債務'), ('NC', '國家賠償'),
        ('TP', '消費爭議'), ('EA', '選舉訴訟'), ('FM', '金融市場'), ('FT', '公平交易'), ('PN', '房地糾紛'),
    )
    
    category = models.CharField(max_length=20, choices=CATEGORYS, 
                                verbose_name=_('Category:'),
                                help_text=_('Please Choose The Category'))

    category_cn = models.CharField(max_length=20, choices=CATEGORYS)

class LawyerSpecialty(models.Model):
    lawyerNo = models.ForeignKey(Lawyer)
    litigations = models.ForeignKey(LitigationType) 
    caseNum = models.IntegerField(null=True, blank=True, default=0)
    
    # custom manager
    objects = LawyerSpecialtyManager()
    
    

'''
using for mail consulting
'''
class UserInquiry(models.Model):
    # tuple
    INCIDENT_TYPE = (
        ('EC', '感情事件'), ('IP', '智慧財產'), ('MD', '醫療糾紛'), ('IW', '網路世界'), ('EP', '毒品問題'),
        ('PC', '支付命令'), ('GP', '政府採購'), ('PE', '環境保護'), ('FC', '詐騙案件'), ('HI', '遺產繼承'),
        ('CI', '公司經營'), ('CD', '車禍糾紛'), ('ID', '保險爭議'), ('RD', '營造工程'), ('BC', '兒少事件'),
        ('SA', '性侵案件'), ('LA', '訴訟程序'), ('LP', '勞資糾紛'), ('BD', '銀行債務'), ('NC', '國家賠償'),
        ('TP', '消費爭議'), ('EA', '選舉訴訟'), ('FM', '金融市場'), ('FT', '公平交易'), ('PN', '房地糾紛'),
    )
    
    INCIDENT_PLACE = (
        ('KEELUNG', '基隆'),
        ('TAIPEI', '台北'),
        ('HSINCHU', '新竹'),
        ('TAICHUNG', '台中'),
        ('TAINAN', '台南'),
        ('YILAN', '宜蘭'),
        ('TAOYUAN', '桃園'),
        ('MIAOLI', '苗栗'),
        ('CHANGHUS', '彰化'),
        ('YUNLIN', '雲林'),
        ('CHIAYI', '嘉義'),
        ('PINGTUNG', '屏東'),
        ('TAITUNG', '台東'),
        ('HUALIEN', '花蓮'),
        ('PENGHU', '澎湖'),
        ('KAOHSIUNG', '高雄'),
        ('NANTOU', '南投'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='inquiry')
    lawyerNo = models.CharField(max_length=32, blank=True, help_text=_('please input the lawyer certification number '))
    
    phone_regex = RegexValidator(regex=r'\d{2,4}\-\d{3,5}\-\d{3,5}$',
                                    message=_("Phone number must be entered in the format xxxx-xxx-xxx or xx-xxxx-xxxx"))
    
    email = models.EmailField(verbose_name=_('email address'), max_length=100, blank=False)
    phoneNumber = models.CharField(verbose_name=_('phone number'), max_length=20, validators=[phone_regex], blank=True)
    incidentPlace = models.CharField(max_length=20, choices=INCIDENT_PLACE, blank=False)
    
    incidentType = models.CharField(max_length=20, choices=INCIDENT_TYPE, blank=False)
    
    dateHappened = models.DateTimeField(_('date of incident happened'), default=timezone.now)
    dateInquiry = models.DateTimeField(_('inquiry date'), default=timezone.now)
    
    inquiryTitle = models.CharField(verbose_name=_('inquiry title'), max_length=20, blank=False)
    inquiryContents = models.TextField(verbose_name=_('inquiry contents'), max_length=65536, blank=False)


class WebStaticContents(models.Model):
    key = models.CharField(max_length=130,blank=False)
    contents = models.TextField(max_length=65536,blank=False)

class Item(models.Model):
    text = models.TextField(default='default')
    
