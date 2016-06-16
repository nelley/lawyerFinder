from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from lawyerFinder.models import *
from lawyerFinder.forms import Lawyer_SearchForm, LitigationTypeForm, BarassociationForm, Lawyer_RegForm
from accounts.forms import *
from django.core.handlers.wsgi import logger
from accounts.models import User
from django.db import IntegrityError, transaction
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


# Create your views here.
def user_login_view(request):
    logger.debug('user login page Start')
    args = {}
    user_loginform = ''
    
    #print request.method
    if request.method == 'POST':
        user_loginform = User_Loginform(request.POST)
        if user_loginform.is_valid():
            id = user_loginform.cleaned_data['username']
            pw = user_loginform.cleaned_data['password']
            
            user = authenticate(username=id, password=pw)
            if user is not None:
                login(request, user)
                if "next" in request.POST and request.POST["next"]:
                    return redirect(request.POST["next"])
                else:
                    return redirect('home')
            else:
                logger.debug('#Login Failed')
                messages.error(request, _('ID or PW mismatching'))
                user_loginform = User_Loginform()
                args = {'user_loginform':user_loginform}
                    
        else:
            logger.debug('Something Wrong When Login')
            args = {'user_loginform':user_loginform}
            
    elif "next" in request.GET: #when write a mail for querying, etc
        user_loginform = User_Loginform() 
        args = {'user_loginform':user_loginform, 
                "next":request.GET['next']}
        
    else:
        user_loginform = User_Loginform()
        args = {'user_loginform':user_loginform}
          
          
    return render_to_response('accounts/user_login.html', 
                              args, 
                              context_instance=RequestContext(request))

@transaction.atomic
def register_lawyer_view(request):
    args = {}
    lawyer_regform = ''
    agreement_regform = ''
    confirm_form = ''
    
        
    if request.method == 'POST' and request.POST['flag'] == '3':
        logger.debug('save user info start')
        
        try:
            with transaction.atomic():
                # insert as a user
                u = User.objects
                u.create_user(username=request.session['id'], 
                              email=request.session['id'], 
                              password=request.session['pw'],
                              active_flag=False)
                # add this ID to gtoup
                insertedu = User.objects.get(username = request.session['id'])
                tmpG = Group.objects.get(name = 'LAWYER')
                insertedu.groups.add(tmpG)
                
                # insert user to lawyer
                l = Lawyer(user=insertedu, 
                           lawyerNo=request.session['lawyerNo'], 
                           gender=request.session['gender'], 
                           premiumType=Lawyer.PREMIUM[0][0], 
                           careerYear=request.session['careerYear'])
                l.save()
                
                # relate areas & fields about this lawyer
                areas = Barassociation.objects.filter(area__in=request.session['regBarAss'])
                LawyerMembership.objects.create_in_bulk(l, areas)
                fields = LitigationType.objects.filter(category__in=request.session['specialty'])
                LawyerSpecialty.objects.create_in_bulk(l, fields)
                
                logger.debug('user added!')
                #clean sessions
                for key in request.session.keys():
                    del request.session[key]
                    
                return HttpResponseRedirect(reverse('home'))
            
        except IntegrityError as e:
            logger.debug('Add Lawyer Failed')
            logger.debug(e.message)
    
    elif request.method == 'POST' and request.POST['flag'] == '2':
        logger.debug('Confirm page Start')
        lawyer_regform = Lawyer_RegForm(request.POST)
        if lawyer_regform.is_valid():
            #get value from POST
            request.session['lawyerNo'] = lawyer_regform.cleaned_data['lawyerNo']
            request.session['gender'] = lawyer_regform.cleaned_data['gender']
            request.session['careerYear'] = lawyer_regform.cleaned_data['careerYear']
            request.session['companyAddress'] = lawyer_regform.cleaned_data['companyAddress']
            request.session['regBarAss'] = lawyer_regform.cleaned_data['regBarAss']
            request.session['specialty'] = lawyer_regform.cleaned_data['specialty']
            
            #display the confirm page's info in dict
            confirm_form = {'Ausername':request.session['id'],
                            'BlawyerNo':request.session['lawyerNo'],
                            'Cgender':request.session['gender'],
                            'DcareerYear':request.session['careerYear'],
                            'EcompanyAddress':request.session['companyAddress'],
                            'FregBarAss':request.session['regBarAss'],
                            'Gspecialty':request.session['specialty'],}
            
            stageflag = '3'
            
        else:
            stageflag = '2'
        
        
    elif request.method == 'POST' and request.POST['flag'] == '1':
        logger.debug('Register page 2 start')
        agreement_regform = User_reg_form(request.POST)
        if agreement_regform.is_valid():# will call clean()
            request.session['id'] = agreement_regform.cleaned_data['username']
            request.session['pw'] = agreement_regform.cleaned_data['password']
        
            lawyer_regform = Lawyer_RegForm()
        
            stageflag = '2'
        else:
            stageflag = '1'
        
        
    else:# display register page
        logger.debug('Register page 1 start')
        # clean session related to registeration
        
        agreement_regform = User_reg_form()
        stageflag = '1'
        
    
    args = {'agreement_regform':agreement_regform,
            'lawyer_regform':lawyer_regform,
            'confirm_form':confirm_form,
            'title' : 'register',
            'stageflag' : stageflag,
            }

    return render_to_response(
        'accounts/register_lawyer.html',
        args,
        context_instance=RequestContext(request)
    )
    
    
def lawyer_login_view(request):
    logger.debug('user login page Start')
    args = {}
    user_loginform = ''
    
    #print request.method
    if request.method == 'POST':
        user_loginform = User_Loginform(request.POST)
        if user_loginform.is_valid():
            id = user_loginform.cleaned_data['username']
            pw = user_loginform.cleaned_data['password']
            
            logger.debug('#Login Process Sarted')
            user = authenticate(username=id, password=pw)
            if user is not None:
                login(request, user)
                if "next" in request.POST and request.POST["next"]:
                    return redirect(request.POST["next"])
                else:
                    #redirect to lawyer management page
                    return redirect('home')
            else:
                logger.debug('#Login Failed')
                messages.error(request, _('ID or PW mismatching'))
                user_loginform = User_Loginform()
                args = {'user_loginform':user_loginform}

        else:
            logger.debug('#Something Wrong When Login!!')
            args = {'user_loginform':user_loginform}
            
    elif "next" in request.GET:
        user_loginform = User_Loginform() 
        args = {"next":request.GET['next']}
        
    else:
        user_loginform = User_Loginform()
        args = {'user_loginform':user_loginform}
          
          
    return render_to_response('accounts/lawyer_login.html', 
                              args, 
                              context_instance=RequestContext(request))
    
    
def repw_view(request):
    args={'title':'repassword'}
    
    return render_to_response(
        'accounts/_base.html',
        args,
        context_instance=RequestContext(request)
    )
    
def user_register_view(request):
    args={}
    
    return render_to_response(
        'base/under_cons.html',
        args,
        context_instance=RequestContext(request)
    )