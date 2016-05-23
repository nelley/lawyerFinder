from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import make_password 
from lawyerFinder.models import Lawyer, LitigationType, Barassociation
from lawyerFinder.forms import Lawyer_SearchForm, LitigationTypeForm, BarassociationForm, Lawyer_RegForm
from accounts.forms import User_reg_form
from django.core.handlers.wsgi import logger



# Create your views here.
def login_view(request):
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
                messages.warning(request, 'error')
        else:
            messages.warning(request, 'error')
        args = {
                'email':request.POST['email'],
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
        
    
    
    elif request.method == 'POST' and request.POST['flag'] == '2':
        logger.debug('Confirm page Start')
        
        request.session['lawyerNo'] = request.POST['lawyerNo']
        request.session['gender'] = request.POST['gender']
        request.session['careerYear'] = request.POST['careerYear']
        request.session['companyAddress'] = request.POST['companyAddress']
        
        request.session['regBarAss'] = request.POST.getlist('regBarAss')
        request.session['specialty'] = request.POST.getlist('specialty')
        #lawyer_regform = Lawyer_RegForm(request.POST, request.FILES) # will call clean_photos
        #if lawyer_regform.is_valid():
        #    lawyer_regform.save()
        #    return HttpResponseRedirect(reverse('home'))
        stageflag = '3'
        
        
    elif request.method == 'POST' and request.POST['flag'] == '1':
        logger.debug('Register page 2 start')
        agreement_regform = User_reg_form(request.POST)
        if agreement_regform.is_valid():# will call clean()
            
            request.session['id'] = request.POST['username']
            request.session['pw'] = request.POST['password']
        
            #make_password()
        
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
