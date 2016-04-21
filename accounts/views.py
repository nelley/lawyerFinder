from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
import logging


# Create your views here.
def login_view(request):
    args = {}
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                if "next" in request.POST and request.POST["next"]:
                    return redirect(request.POST["next"])
                else:
                    return redirect('hello')
            else:
                messages.warning(request, 'error')
        else:
            messages.warning(request, 'error')
        args = {
                'email':request.POST['email'],
                'next': request.POST['next']
                }
    elif "next" in request.GET:
          args = {"next":request.GET['next']}
    return render_to_response('accounts/login.html', args, context_instance=RequestContext(request))





