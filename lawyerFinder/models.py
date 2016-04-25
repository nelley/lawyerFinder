# coding: utf-8
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


class LawyerMembershipManager(models.Manager):
    def create_in_bulk(self, target, values):
        base_sql = "INSERT INTO lawyerfinder_lawyermembership (lawyerId_id, barAssociation_id, date_joined) VALUES (%s, %s, %s) "
        now = timezone.now().strftime("%Y-%m-%d")
        
        values_data = []
        for value in values:
            tmpTuple = (target.userId_id, value.id, now)
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
    area = models.CharField(max_length=20, choices=AREAS)


# person
class Lawyer(models.Model):
    GENDER = (
        ('MALE', '男性'),
        ('FEMALE', '女性'),
    )

    userId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='foobar')
    lawyerId = models.CharField(max_length=32, blank=False)
    premiumType = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER)
    careerYear = models.IntegerField(null=True, blank=True, default=0)
    companyAddress = models.CharField(max_length=50)
    regBarAss = models.ManyToManyField('Barassociation', through='LawyerMembership',
                                     blank=False, 
                                     help_text=_('the area that lawyer have been registered in'), 
                                     verbose_name=_('Registered Bar Association'))
    
    specialty = models.ManyToManyField('LitigationType', through='LawyerSpecialty',
                                     blank=False, 
                                     help_text=_('the strong field of this lawyer'), 
                                     verbose_name=_('the strong field of this lawyer'))
    #phoneNumber
    #age
    
    def __str__(self):
        #return "%s (%s)" % (self.lawyerId, ", ".join(litigationtype.category for litigationtype in self.specialty.all()))
        return "%s (%s)" % (self.lawyerId, ", ".join(barassociation.area 
                                                     for barassociation in self.regBarAss.all()))
    
    
# membership
class LawyerMembership(models.Model):
    lawyerId = models.ForeignKey(Lawyer)
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
    #specialty = models.CharField(max_length=20, choices=CATEGORYS)
    category = models.CharField(max_length=20, choices=CATEGORYS)
    #experts = models.ManyToManyField('Lawyer', through='LawyerSpecialty',
    #                                 blank=False, 
    #                                 help_text=_('the cases that lawyer have been done'), 
    #                                 verbose_name=_('the cases that lawyer have been done'))

class LawyerSpecialty(models.Model):
    lawyerId = models.ForeignKey(Lawyer)
    litigations = models.ForeignKey(LitigationType) 
    caseNum = models.IntegerField(null=True, blank=True, default=0)
