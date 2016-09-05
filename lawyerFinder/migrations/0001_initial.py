# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import ckeditor.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Barassociation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.CharField(help_text='Please Choose The Area', max_length=20, verbose_name='AREA:', choices=[(b'KEELUNG', b'\xe5\x9f\xba\xe9\x9a\x86'), (b'TAIPEI', b'\xe5\x8f\xb0\xe5\x8c\x97'), (b'HSINCHU', b'\xe6\x96\xb0\xe7\xab\xb9'), (b'TAICHUNG', b'\xe5\x8f\xb0\xe4\xb8\xad'), (b'TAINAN', b'\xe5\x8f\xb0\xe5\x8d\x97'), (b'YILAN', b'\xe5\xae\x9c\xe8\x98\xad'), (b'TAOYUAN', b'\xe6\xa1\x83\xe5\x9c\x92'), (b'MIAOLI', b'\xe8\x8b\x97\xe6\xa0\x97'), (b'CHANGHUS', b'\xe5\xbd\xb0\xe5\x8c\x96'), (b'YUNLIN', b'\xe9\x9b\xb2\xe6\x9e\x97'), (b'CHIAYI', b'\xe5\x98\x89\xe7\xbe\xa9'), (b'PINGTUNG', b'\xe5\xb1\x8f\xe6\x9d\xb1'), (b'TAITUNG', b'\xe5\x8f\xb0\xe6\x9d\xb1'), (b'HUALIEN', b'\xe8\x8a\xb1\xe8\x93\xae'), (b'PENGHU', b'\xe6\xbe\x8e\xe6\xb9\x96'), (b'KAOHSIUNG', b'\xe9\xab\x98\xe9\x9b\x84'), (b'NANTOU', b'\xe5\x8d\x97\xe6\x8a\x95')])),
                ('area_cn', models.CharField(max_length=20, choices=[(b'KEELUNG', b'\xe5\x9f\xba\xe9\x9a\x86'), (b'TAIPEI', b'\xe5\x8f\xb0\xe5\x8c\x97'), (b'HSINCHU', b'\xe6\x96\xb0\xe7\xab\xb9'), (b'TAICHUNG', b'\xe5\x8f\xb0\xe4\xb8\xad'), (b'TAINAN', b'\xe5\x8f\xb0\xe5\x8d\x97'), (b'YILAN', b'\xe5\xae\x9c\xe8\x98\xad'), (b'TAOYUAN', b'\xe6\xa1\x83\xe5\x9c\x92'), (b'MIAOLI', b'\xe8\x8b\x97\xe6\xa0\x97'), (b'CHANGHUS', b'\xe5\xbd\xb0\xe5\x8c\x96'), (b'YUNLIN', b'\xe9\x9b\xb2\xe6\x9e\x97'), (b'CHIAYI', b'\xe5\x98\x89\xe7\xbe\xa9'), (b'PINGTUNG', b'\xe5\xb1\x8f\xe6\x9d\xb1'), (b'TAITUNG', b'\xe5\x8f\xb0\xe6\x9d\xb1'), (b'HUALIEN', b'\xe8\x8a\xb1\xe8\x93\xae'), (b'PENGHU', b'\xe6\xbe\x8e\xe6\xb9\x96'), (b'KAOHSIUNG', b'\xe9\xab\x98\xe9\x9b\x84'), (b'NANTOU', b'\xe5\x8d\x97\xe6\x8a\x95')])),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default=b'default')),
            ],
        ),
        migrations.CreateModel(
            name='Lawyer',
            fields=[
                ('user', models.OneToOneField(related_name='foobar', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('lawyerNo', models.CharField(help_text='please input the lawyer certification number ', max_length=32, blank=True)),
                ('premiumType', models.CharField(default=b'1', max_length=30, blank=True)),
                ('gender', models.CharField(blank=True, max_length=20, choices=[(b'M', b'\xe7\x94\xb7\xe6\x80\xa7'), (b'F', b'\xe5\xa5\xb3\xe6\x80\xa7')])),
                ('careerYear', models.IntegerField(default=0, help_text='please input the career year', null=True, blank=True)),
                ('companyAddress', models.CharField(help_text="please input the company's address", max_length=50, blank=True)),
                ('phoneNumber', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(regex=b'\\d{2,4}\\-\\d{3,5}\\-\\d{3,5}$', message='Phone number must be entered in the format xxxx-xxx-xxx or xx-xxxx-xxxx')])),
                ('thumbnail', models.ImageField(upload_to=b'', max_length=255, verbose_name='thumbnail', blank=True)),
                ('photos', models.ImageField(upload_to=b'/home/nelley/Downloads/', max_length=255, verbose_name='image', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LawyerMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateField(default=datetime.date.today, null=True)),
                ('barAssociation', models.ForeignKey(to='lawyerFinder.Barassociation')),
            ],
        ),
        migrations.CreateModel(
            name='LawyerSpecialty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caseNum', models.IntegerField(default=0, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LitigationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(help_text='Please Choose The Category', max_length=20, verbose_name='Category:', choices=[(b'EC', b'\xe6\x84\x9f\xe6\x83\x85\xe4\xba\x8b\xe4\xbb\xb6'), (b'IP', b'\xe6\x99\xba\xe6\x85\xa7\xe8\xb2\xa1\xe7\x94\xa2'), (b'MD', b'\xe9\x86\xab\xe7\x99\x82\xe7\xb3\xbe\xe7\xb4\x9b'), (b'IW', b'\xe7\xb6\xb2\xe8\xb7\xaf\xe4\xb8\x96\xe7\x95\x8c'), (b'EP', b'\xe6\xaf\x92\xe5\x93\x81\xe5\x95\x8f\xe9\xa1\x8c'), (b'PC', b'\xe6\x94\xaf\xe4\xbb\x98\xe5\x91\xbd\xe4\xbb\xa4'), (b'GP', b'\xe6\x94\xbf\xe5\xba\x9c\xe6\x8e\xa1\xe8\xb3\xbc'), (b'PE', b'\xe7\x92\xb0\xe5\xa2\x83\xe4\xbf\x9d\xe8\xad\xb7'), (b'FC', b'\xe8\xa9\x90\xe9\xa8\x99\xe6\xa1\x88\xe4\xbb\xb6'), (b'HI', b'\xe9\x81\xba\xe7\x94\xa2\xe7\xb9\xbc\xe6\x89\xbf'), (b'CI', b'\xe5\x85\xac\xe5\x8f\xb8\xe7\xb6\x93\xe7\x87\x9f'), (b'CD', b'\xe8\xbb\x8a\xe7\xa6\x8d\xe7\xb3\xbe\xe7\xb4\x9b'), (b'ID', b'\xe4\xbf\x9d\xe9\x9a\xaa\xe7\x88\xad\xe8\xad\xb0'), (b'RD', b'\xe7\x87\x9f\xe9\x80\xa0\xe5\xb7\xa5\xe7\xa8\x8b'), (b'BC', b'\xe5\x85\x92\xe5\xb0\x91\xe4\xba\x8b\xe4\xbb\xb6'), (b'SA', b'\xe6\x80\xa7\xe4\xbe\xb5\xe6\xa1\x88\xe4\xbb\xb6'), (b'LA', b'\xe8\xa8\xb4\xe8\xa8\x9f\xe7\xa8\x8b\xe5\xba\x8f'), (b'LP', b'\xe5\x8b\x9e\xe8\xb3\x87\xe7\xb3\xbe\xe7\xb4\x9b'), (b'BD', b'\xe9\x8a\x80\xe8\xa1\x8c\xe5\x82\xb5\xe5\x8b\x99'), (b'NC', b'\xe5\x9c\x8b\xe5\xae\xb6\xe8\xb3\xa0\xe5\x84\x9f'), (b'TP', b'\xe6\xb6\x88\xe8\xb2\xbb\xe7\x88\xad\xe8\xad\xb0'), (b'EA', b'\xe9\x81\xb8\xe8\x88\x89\xe8\xa8\xb4\xe8\xa8\x9f'), (b'FM', b'\xe9\x87\x91\xe8\x9e\x8d\xe5\xb8\x82\xe5\xa0\xb4'), (b'FT', b'\xe5\x85\xac\xe5\xb9\xb3\xe4\xba\xa4\xe6\x98\x93'), (b'PN', b'\xe6\x88\xbf\xe5\x9c\xb0\xe7\xb3\xbe\xe7\xb4\x9b')])),
                ('category_cn', models.CharField(max_length=20, choices=[(b'EC', b'\xe6\x84\x9f\xe6\x83\x85\xe4\xba\x8b\xe4\xbb\xb6'), (b'IP', b'\xe6\x99\xba\xe6\x85\xa7\xe8\xb2\xa1\xe7\x94\xa2'), (b'MD', b'\xe9\x86\xab\xe7\x99\x82\xe7\xb3\xbe\xe7\xb4\x9b'), (b'IW', b'\xe7\xb6\xb2\xe8\xb7\xaf\xe4\xb8\x96\xe7\x95\x8c'), (b'EP', b'\xe6\xaf\x92\xe5\x93\x81\xe5\x95\x8f\xe9\xa1\x8c'), (b'PC', b'\xe6\x94\xaf\xe4\xbb\x98\xe5\x91\xbd\xe4\xbb\xa4'), (b'GP', b'\xe6\x94\xbf\xe5\xba\x9c\xe6\x8e\xa1\xe8\xb3\xbc'), (b'PE', b'\xe7\x92\xb0\xe5\xa2\x83\xe4\xbf\x9d\xe8\xad\xb7'), (b'FC', b'\xe8\xa9\x90\xe9\xa8\x99\xe6\xa1\x88\xe4\xbb\xb6'), (b'HI', b'\xe9\x81\xba\xe7\x94\xa2\xe7\xb9\xbc\xe6\x89\xbf'), (b'CI', b'\xe5\x85\xac\xe5\x8f\xb8\xe7\xb6\x93\xe7\x87\x9f'), (b'CD', b'\xe8\xbb\x8a\xe7\xa6\x8d\xe7\xb3\xbe\xe7\xb4\x9b'), (b'ID', b'\xe4\xbf\x9d\xe9\x9a\xaa\xe7\x88\xad\xe8\xad\xb0'), (b'RD', b'\xe7\x87\x9f\xe9\x80\xa0\xe5\xb7\xa5\xe7\xa8\x8b'), (b'BC', b'\xe5\x85\x92\xe5\xb0\x91\xe4\xba\x8b\xe4\xbb\xb6'), (b'SA', b'\xe6\x80\xa7\xe4\xbe\xb5\xe6\xa1\x88\xe4\xbb\xb6'), (b'LA', b'\xe8\xa8\xb4\xe8\xa8\x9f\xe7\xa8\x8b\xe5\xba\x8f'), (b'LP', b'\xe5\x8b\x9e\xe8\xb3\x87\xe7\xb3\xbe\xe7\xb4\x9b'), (b'BD', b'\xe9\x8a\x80\xe8\xa1\x8c\xe5\x82\xb5\xe5\x8b\x99'), (b'NC', b'\xe5\x9c\x8b\xe5\xae\xb6\xe8\xb3\xa0\xe5\x84\x9f'), (b'TP', b'\xe6\xb6\x88\xe8\xb2\xbb\xe7\x88\xad\xe8\xad\xb0'), (b'EA', b'\xe9\x81\xb8\xe8\x88\x89\xe8\xa8\xb4\xe8\xa8\x9f'), (b'FM', b'\xe9\x87\x91\xe8\x9e\x8d\xe5\xb8\x82\xe5\xa0\xb4'), (b'FT', b'\xe5\x85\xac\xe5\xb9\xb3\xe4\xba\xa4\xe6\x98\x93'), (b'PN', b'\xe6\x88\xbf\xe5\x9c\xb0\xe7\xb3\xbe\xe7\xb4\x9b')])),
            ],
        ),
        migrations.CreateModel(
            name='UserInquiry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lawyerNo', models.CharField(help_text='please input the lawyer certification number ', max_length=32, blank=True)),
                ('email', models.EmailField(max_length=100, verbose_name='email address')),
                ('phoneNumber', models.CharField(blank=True, max_length=20, verbose_name='phone number', validators=[django.core.validators.RegexValidator(regex=b'\\d{2,4}\\-\\d{3,5}\\-\\d{3,5}$', message='Phone number must be entered in the format xxxx-xxx-xxx or xx-xxxx-xxxx')])),
                ('incidentPlace', models.CharField(max_length=20, choices=[(b'KEELUNG', b'\xe5\x9f\xba\xe9\x9a\x86'), (b'TAIPEI', b'\xe5\x8f\xb0\xe5\x8c\x97'), (b'HSINCHU', b'\xe6\x96\xb0\xe7\xab\xb9'), (b'TAICHUNG', b'\xe5\x8f\xb0\xe4\xb8\xad'), (b'TAINAN', b'\xe5\x8f\xb0\xe5\x8d\x97'), (b'YILAN', b'\xe5\xae\x9c\xe8\x98\xad'), (b'TAOYUAN', b'\xe6\xa1\x83\xe5\x9c\x92'), (b'MIAOLI', b'\xe8\x8b\x97\xe6\xa0\x97'), (b'CHANGHUS', b'\xe5\xbd\xb0\xe5\x8c\x96'), (b'YUNLIN', b'\xe9\x9b\xb2\xe6\x9e\x97'), (b'CHIAYI', b'\xe5\x98\x89\xe7\xbe\xa9'), (b'PINGTUNG', b'\xe5\xb1\x8f\xe6\x9d\xb1'), (b'TAITUNG', b'\xe5\x8f\xb0\xe6\x9d\xb1'), (b'HUALIEN', b'\xe8\x8a\xb1\xe8\x93\xae'), (b'PENGHU', b'\xe6\xbe\x8e\xe6\xb9\x96'), (b'KAOHSIUNG', b'\xe9\xab\x98\xe9\x9b\x84'), (b'NANTOU', b'\xe5\x8d\x97\xe6\x8a\x95')])),
                ('incidentType', models.CharField(max_length=20, choices=[(b'EC', b'\xe6\x84\x9f\xe6\x83\x85\xe4\xba\x8b\xe4\xbb\xb6'), (b'IP', b'\xe6\x99\xba\xe6\x85\xa7\xe8\xb2\xa1\xe7\x94\xa2'), (b'MD', b'\xe9\x86\xab\xe7\x99\x82\xe7\xb3\xbe\xe7\xb4\x9b'), (b'IW', b'\xe7\xb6\xb2\xe8\xb7\xaf\xe4\xb8\x96\xe7\x95\x8c'), (b'EP', b'\xe6\xaf\x92\xe5\x93\x81\xe5\x95\x8f\xe9\xa1\x8c'), (b'PC', b'\xe6\x94\xaf\xe4\xbb\x98\xe5\x91\xbd\xe4\xbb\xa4'), (b'GP', b'\xe6\x94\xbf\xe5\xba\x9c\xe6\x8e\xa1\xe8\xb3\xbc'), (b'PE', b'\xe7\x92\xb0\xe5\xa2\x83\xe4\xbf\x9d\xe8\xad\xb7'), (b'FC', b'\xe8\xa9\x90\xe9\xa8\x99\xe6\xa1\x88\xe4\xbb\xb6'), (b'HI', b'\xe9\x81\xba\xe7\x94\xa2\xe7\xb9\xbc\xe6\x89\xbf'), (b'CI', b'\xe5\x85\xac\xe5\x8f\xb8\xe7\xb6\x93\xe7\x87\x9f'), (b'CD', b'\xe8\xbb\x8a\xe7\xa6\x8d\xe7\xb3\xbe\xe7\xb4\x9b'), (b'ID', b'\xe4\xbf\x9d\xe9\x9a\xaa\xe7\x88\xad\xe8\xad\xb0'), (b'RD', b'\xe7\x87\x9f\xe9\x80\xa0\xe5\xb7\xa5\xe7\xa8\x8b'), (b'BC', b'\xe5\x85\x92\xe5\xb0\x91\xe4\xba\x8b\xe4\xbb\xb6'), (b'SA', b'\xe6\x80\xa7\xe4\xbe\xb5\xe6\xa1\x88\xe4\xbb\xb6'), (b'LA', b'\xe8\xa8\xb4\xe8\xa8\x9f\xe7\xa8\x8b\xe5\xba\x8f'), (b'LP', b'\xe5\x8b\x9e\xe8\xb3\x87\xe7\xb3\xbe\xe7\xb4\x9b'), (b'BD', b'\xe9\x8a\x80\xe8\xa1\x8c\xe5\x82\xb5\xe5\x8b\x99'), (b'NC', b'\xe5\x9c\x8b\xe5\xae\xb6\xe8\xb3\xa0\xe5\x84\x9f'), (b'TP', b'\xe6\xb6\x88\xe8\xb2\xbb\xe7\x88\xad\xe8\xad\xb0'), (b'EA', b'\xe9\x81\xb8\xe8\x88\x89\xe8\xa8\xb4\xe8\xa8\x9f'), (b'FM', b'\xe9\x87\x91\xe8\x9e\x8d\xe5\xb8\x82\xe5\xa0\xb4'), (b'FT', b'\xe5\x85\xac\xe5\xb9\xb3\xe4\xba\xa4\xe6\x98\x93'), (b'PN', b'\xe6\x88\xbf\xe5\x9c\xb0\xe7\xb3\xbe\xe7\xb4\x9b')])),
                ('dateHappened', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date of incident happened')),
                ('dateInquiry', models.DateTimeField(default=django.utils.timezone.now, verbose_name='inquiry date')),
                ('inquiryTitle', models.CharField(max_length=20, verbose_name='inquiry title')),
                ('inquiryContents', models.TextField(max_length=65536, verbose_name='inquiry contents')),
                ('user', models.ForeignKey(related_name='inquiry', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WebStaticContents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=130)),
                ('contents', models.TextField(max_length=65536)),
            ],
        ),
        migrations.CreateModel(
            name='Lawyer_infos',
            fields=[
                ('lawyer', models.OneToOneField(related_name='lawyer_info', primary_key=True, serialize=False, to='lawyerFinder.Lawyer')),
                ('basic', ckeditor.fields.RichTextField(max_length=130, blank=True)),
                ('strongFields', ckeditor.fields.RichTextField(max_length=130, blank=True)),
                ('finishedCases', ckeditor.fields.RichTextField(max_length=130, blank=True)),
                ('feeStd', ckeditor.fields.RichTextField(max_length=130, blank=True)),
                ('companyInfos', ckeditor.fields.RichTextField(max_length=130, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='lawyerspecialty',
            name='lawyerNo',
            field=models.ForeignKey(to='lawyerFinder.Lawyer'),
        ),
        migrations.AddField(
            model_name='lawyerspecialty',
            name='litigations',
            field=models.ForeignKey(to='lawyerFinder.LitigationType'),
        ),
        migrations.AddField(
            model_name='lawyermembership',
            name='lawyerNo',
            field=models.ForeignKey(to='lawyerFinder.Lawyer'),
        ),
        migrations.AddField(
            model_name='lawyer',
            name='regBarAss',
            field=models.ManyToManyField(help_text='the area that lawyer have been registered in', to='lawyerFinder.Barassociation', verbose_name='Registered Bar Association', through='lawyerFinder.LawyerMembership', blank=True),
        ),
        migrations.AddField(
            model_name='lawyer',
            name='specialty',
            field=models.ManyToManyField(help_text='the strong field of this lawyer', to='lawyerFinder.LitigationType', verbose_name='the strong field of this lawyer', through='lawyerFinder.LawyerSpecialty', blank=True),
        ),
    ]
