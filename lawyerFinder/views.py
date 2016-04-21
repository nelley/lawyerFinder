from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
import logging
from accounts.cus_decorators import group_required


@group_required('STAFF')
def home(request):
    return render_to_response(
        # template name
        'lawyerFinder/index.html', 
        {
            # [dictionary]values that passes to the front end
            'title' : 'lawyer!',
            #'form': form,
            #'formMember' : formMember,
            #'userForm' : userForm
        }
    )