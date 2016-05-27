from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from lawyerFinder.models import *
from lawyerFinder.forms import Lawyer_SearchForm, LitigationTypeForm, BarassociationForm, Lawyer_RegForm
from accounts.forms import User_reg_form
from django.core.handlers.wsgi import logger
from accounts.models import User
from django.db import IntegrityError, transaction
from django.contrib.auth.models import Group




# Create your views here.
def login_view(request):
    logger.debug('user login page Start')
    args = {}
    
    # check whether logged in or not
    
    #print request.method
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                if "next" in request.POST and request.POST["next"]:
                    return redirect(request.POST["next"])
                else:
                    return redirect('home')
            else:
                logger.debug('This user is inactive!!')
                #redirect to the inactive page || limited some views on a page
                messages.warning(request, 'error')
        else:
            logger.debug('This Account is Not Our User!!')
            #show the error msg about id||pw is wrong!!
            messages.warning(request, 'error')
        args = {
                #'email':request.POST['email'],
                'next': request.POST['next'],
                }
    elif "next" in request.GET:
          args = {"next":request.GET['next']}
          
    return render_to_response('accounts/login.html', args, context_instance=RequestContext(request))


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
