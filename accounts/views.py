from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from lawyerFinder.models import *
from lawyerFinder.forms import Lawyer_SearchForm, LitigationTypeForm, BarassociationForm, Lawyer_RegForm
from accounts.forms import *
from accounts.models import *
from django.core.handlers.wsgi import logger
from django.db import IntegrityError, transaction
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from common.utilities import *
import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash


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
    lawyer_nameform = ''
    confirm_form = ''
    DEFAULT_INFOS = '<h4>Your Service</h4><p>Please Edit Your Service</p>'

    if request.method == 'POST' and request.POST['flag'] == '3':
        logger.debug('save user info start')
        
        try:
            with transaction.atomic():
                # insert as a user
                u = User.objects
                u.create_user(username=request.session['id'], 
                              first_name=request.session['first_name'],
                              last_name=request.session['last_name'],
                              email=request.session['id'],
                              password=request.session['pw'],
                              active_flag=False)
                # add this ID to group
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
                
                # add default data to lawyer_info table
                l_infos =Lawyer_infos(lawyer_id=l.user_id,
                             basic=DEFAULT_INFOS,
                             strongFields=DEFAULT_INFOS,
                             finishedCases=DEFAULT_INFOS,
                             feeStd=DEFAULT_INFOS,
                             companyInfos=DEFAULT_INFOS)
                l_infos.save()
                
                messages.success(request, _('Lawyer Member Registeration Successed'))
                logger.debug('user added!')
                #clean sessions
                for key in request.session.keys():
                    del request.session[key]
                    
                return HttpResponseRedirect(reverse('home'))
            
        except IntegrityError as e:
            messages.error(request, _('Lawyer Member Registeration Failed'))
            logger.debug('Add Lawyer Failed')
            logger.debug(e.message)
            return HttpResponseRedirect(reverse('home'))
    
    elif request.method == 'POST' and request.POST['flag'] == '2':
        logger.debug('Confirm page Start')
        lawyer_regform = Lawyer_RegForm(request, request.POST)
        lawyer_nameform = Lawyer_Nameform(request.POST)
        
        if lawyer_nameform.is_valid():
            request.session['first_name'] = lawyer_nameform.cleaned_data['first_name']
            request.session['last_name'] = lawyer_nameform.cleaned_data['last_name']
        
        if lawyer_regform.is_valid():
            #get value from POST
            request.session['lawyerNo'] = lawyer_regform.cleaned_data['lawyerNo']
            request.session['gender'] = lawyer_regform.cleaned_data['gender']
            request.session['careerYear'] = lawyer_regform.cleaned_data['careerYear']
            request.session['companyAddress'] = lawyer_regform.cleaned_data['companyAddress']
            request.session['phoneNumber'] = lawyer_regform.cleaned_data['phoneNumber']
            request.session['regBarAss'] = lawyer_regform.cleaned_data['regBarAss']
            request.session['specialty'] = lawyer_regform.cleaned_data['specialty']
            
            #display the confirm page's info in dict
            confirm_form = {'Afirstname':request.session['first_name'],
                            'Blastname':request.session['last_name'],
                            'Cusername':request.session['id'],
                            'DlawyerNo':request.session['lawyerNo'],
                            'Egender':request.session['gender'],
                            'FcareerYear':request.session['careerYear'],
                            'GcompanyAddress':request.session['companyAddress'],
                            'HphoneNumber':request.session['phoneNumber'],
                            'IregBarAss':request.session['regBarAss'],
                            'Jspecialty':request.session['specialty'],}
            
            stageflag = '3'
            
        else:
            stageflag = '2'
            
    elif request.method == 'POST' and request.POST['flag'] == '1':
        logger.debug('Register page 2 start')
        agreement_regform = User_reg_form(request.POST, request=request)
        if agreement_regform.is_valid():# will call clean()
            request.session['id'] = agreement_regform.cleaned_data['username']
            request.session['pw'] = agreement_regform.cleaned_data['password']
        
            lawyer_regform = Lawyer_RegForm(request)
            lawyer_nameform = Lawyer_Nameform()
            
            stageflag = '2'
        else:
            stageflag = '1'
        
    else:# display register page
        logger.debug('Register page 1 start')
        # clean session related to registeration
        agreement_regform = User_reg_form()
        
        stageflag = '1'
        
    args = {'agreement_regform':agreement_regform,
            'lawyer_nameform':lawyer_nameform,
            'lawyer_regform':lawyer_regform,
            'confirm_form':confirm_form,
            'title' : 'register',
            'service_url':SITE_URL+'site_service_rule/',
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
    logger.debug('repassword Start')
    args={'title':'repassword'}
    
    if request.POST:
        emailID = request.POST['username']
        type = request.POST['type']
        re = User.objects.filter(username = emailID)
        # user is existed or not
        if re:
            is_active = re.is_active
            # if user request repassword
            if type == 'REPW':
                if is_active == True:
                    # generate new pw
                    password = User.objects.make_random_password(length=12,
                                                                 allowed_chars='!@#$%^&*abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                    # sent mail successed
                    mailSender(mail_to=emailID, pw=password)
                    # update new pw to DB
                    re.set_password(password)
                    re.save()
                    messages.success(request, _('Please check your new pw in your email account'))
                else:
                    messages.warning(request, _("This ID has not been activated. Please check your mailbox"))
            # if user request resend confirm mail
            elif(type == 'RECO'):
                if is_active == True:
                    messages.warning(request, _("This ID has been activated."))
                else:
                    try:
                        with transaction.atomic():
                            token = gen_tokens(emailID)
                            RegistTokens.objects.create(email=emailID, registkey=token)
                            # send mail by SES with new token
                            mailSender(mail_to=emailID, token=token)
                            messages.success(request, _('Please Check The Comfirmation Mail In Your Mailbox'))
                    except IntegrityError as e:
                        messages.error(request, _('ReComfirmation Failed'))
                        logger.debug('ReComfirmation Failed')
                        logger.debug(e.message)
        else:
            messages.warning(request, _('This Email has not been registered'))
    
    return render_to_response(
        'accounts/_base.html',
        args,
        context_instance=RequestContext(request)
    )
    

def user_repw(request):
    args={}
    user_repw_form = ''
    repw_u = User.objects.get(id=request.session['_auth_user_id'])
    
    if request.method == 'POST':
        logger.debug('change pw start')
        user_repw_form= User_repw_form(request.POST)
        
        if user_repw_form.is_valid():
            logger.debug('change pw form validation passed')
            
            if repw_u.check_password(user_repw_form.cleaned_data['oldPassword']):
                repw_u.set_password(user_repw_form.cleaned_data['newPassword'])
                repw_u.save(update_fields=["password"])
                update_session_auth_hash(request, repw_u)
                
                logger.debug('New PW Is Updated')
                messages.success(request, _('New PW Is Updated'))
            else:
                logger.debug('Old PW does not correct')
                messages.error(request, _('Old PW does not correct'))
            
            return render_to_response(
                                        'accounts/user_repw.html',
                                        {'user_repw_form': user_repw_form,
                                         'user_email':repw_u.email},
                                        context_instance=RequestContext(request))
    else:
        user_repw_form = User_repw_form()
    
    return render_to_response(
        'accounts/user_repw.html',
        {'user_repw_form': user_repw_form,
         'user_email':repw_u.email},
        context_instance=RequestContext(request))

@transaction.atomic
def user_register_view(request):
    logger.debug('User register Start')
    user_reg_form=''
    
    if request.POST:
        user_reg_regform = User_reg_form(request.POST, request=request)
        if user_reg_regform.is_valid():
            tid = user_reg_regform.cleaned_data['username']
            tpw = user_reg_regform.cleaned_data['password']
            logger.debug('save user info start')
            try:
                with transaction.atomic():
                    # insert as a user
                    u = User.objects
                    u.create_user(username=tid, 
                                  email=tid, 
                                  password=tpw,
                                  active_flag=False)
                    # add this ID to group
                    insertedu = User.objects.get(username = tid)
                    tmpG = Group.objects.get(name = 'ORDINARYUSER')
                    insertedu.groups.add(tmpG)
                    
                    # insert token to table
                    token = gen_tokens(tid)
                    RegistTokens.objects.create(email=tid, registkey=token)
                    
                    # send mail by SES with new token
                    user_regist_mailSender(mail_to=tid, token=token)
                    messages.success(request, _('Please Check The Comfirmation Mail In Your Mailbox'))
                    
            except IntegrityError as e:
                messages.error(request, _('User Member Registeration Failed'))
                logger.debug('Add Lawyer Failed')
                logger.debug(e.message)

            return redirect('home')
            
        logger.debug('input validation failed')
        args={'user_reg_form':user_reg_regform,
              'service_url':SITE_URL+'site_service_rule/',}
    else:
        user_reg_form = User_reg_form()
        args={'user_reg_form':user_reg_form,
              'service_url':SITE_URL+'site_service_rule/',}
    
    
    return render_to_response(
        'accounts/register_user.html',
        args,
        context_instance=RequestContext(request)
    )
    
    
def user_confirm(request, registkey):
    try:
        emailId = RegistTokens.objects.get(registkey=registkey)
        if emailId:
            now = datetime.datetime.now()
            if (now - emailId.created_at).total_seconds() > 60*60:#over 1 hour
                messages.error(request, _('Invalid register key due to exceed time limitation'))
            else:
                u = User.objects.get(username=emailId.email)
                u.is_active = 1
                u.save()
                messages.success(request, _('Account activated'))
    except IntegrityError as e:
        logger.debug('DB Error!') 
    except RegistTokens.DoesNotExist:
        messages.error(request, _('Register Key does not exist'))
    
    return redirect('home')
