from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from lawyerFinder.models import Lawyer, LitigationType, Barassociation
from lawyerFinder.forms import Lawyer_SearchForm, LitigationTypeForm, BarassociationForm, Lawyer_RegForm
from lawyerFinder.forms import Lawyer_RegForm
import logging


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



def register_view(request):
    args = {}
    
    if request.method == 'POST':
        lawyer_regform = Lawyer_RegForm(request.POST, request.FILES) # will call clean_photos
        if lawyer_regform.is_valid():
            print 'file check ok'
            return HttpResponseRedirect(reverse('home'))
            
    #elif request.method == 'GET':# display register page
    else:# display register page
        lawyer_regform = Lawyer_RegForm()
    
    args = {'lawyer_regform':lawyer_regform,
            'title' : 'register',
            }

    return render_to_response(
        'accounts/register.html',
        args,
        context_instance=RequestContext(request)
    )
