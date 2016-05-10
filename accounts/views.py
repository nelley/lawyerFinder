from django.shortcuts import render, redirect, render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from lawyerFinder.models import Lawyer, LitigationType, Barassociation
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
    
    args = []
    redirect = ''
    
    if request.method == 'POST':
        form = Lawyer_RegForm(request.POST, request.FILES)
        if form.is_valid():
            print 'file check ok'
            #messages.add_message(request, messages.SUCCESS, "Image Saved")
        else:
            print 'file check fail'
            print form.errors
            
        redirect = 'base/index.html'
        
    elif request.method == 'GET':# display register page
        # template name
        redirect = 'accounts/register.html'


        lawyer_regform = Lawyer_RegForm()
        
        #redirect = 'lawyerFinder/_index.html'
        args = {'lawyer_regform':lawyer_regform,
                'title' : 'register',
                }

    return render_to_response(
        redirect,
        args,
        context_instance=RequestContext(request)
    )
