from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from lawyerFinder.models import Lawyer, LitigationType, Barassociation
from lawyerFinder.forms import Lawyer_SearchForm, LitigationTypeForm, BarassociationForm, Lawyer_RegForm
from accounts.forms import User_reg_form
from django.core.handlers.wsgi import logger
from accounts.models import User



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
                messages.warning(request, 'error')
        else:
            logger.debug('This Account is Not Our User!!')
            messages.warning(request, 'error')
        args = {
                #'email':request.POST['email'],
                'next': request.POST['next'],
                }
    elif "next" in request.GET:
          args = {"next":request.GET['next']}
          
    return render_to_response('accounts/login.html', args, context_instance=RequestContext(request))



def register_lawyer_view(request):
    args = {}
    lawyer_regform = ''
    agreement_regform = ''
        
        
    
    if request.method == 'POST' and request.POST['flag'] == '3':
        logger.debug('save user info start')
        #agreement_regform = User_reg_form(initial={'username':request.session['id'],
        #                                           'password':request.session['pw'],})
        

        u = User.objects
        u.create_user(username=request.session['id'], 
                      email=request.session['id'], 
                      password=request.session['pw'],
                      active_flag=False)
        
        print 'user added!'
        #agreement_regform.save_custom()
        #lawyer_regform.save_custom()
        
        #agreement_regform.save()
        #lawyer_regform.save()
        # 
        
        
        stageflag = '4'
    
    elif request.method == 'POST' and request.POST['flag'] == '2':
        logger.debug('Confirm page Start')
        lawyer_regform = Lawyer_RegForm(request.POST)
        if lawyer_regform.is_valid():
            request.session['lawyerNo'] = lawyer_regform.cleaned_data['lawyerNo']
            request.session['gender'] = lawyer_regform.cleaned_data['gender']
            request.session['careerYear'] = lawyer_regform.cleaned_data['careerYear']
            request.session['companyAddress'] = lawyer_regform.cleaned_data['companyAddress']
            
            request.session['regBarAss'] = lawyer_regform.cleaned_data['regBarAss']
            request.session['specialty'] = lawyer_regform.cleaned_data['specialty']
            
            stageflag = '3'
        #lawyer_regform = Lawyer_RegForm(request.POST, request.FILES) # will call clean_photos
        #if lawyer_regform.is_valid():
        #    lawyer_regform.save()
        #    return HttpResponseRedirect(reverse('home'))
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
            'title' : 'register',
            'stageflag' : stageflag,
            }

    return render_to_response(
        'accounts/register_lawyer.html',
        args,
        context_instance=RequestContext(request)
    )
