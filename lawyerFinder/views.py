from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
import logging
import datetime
from accounts.cus_decorators import group_required
from lawyerFinder.forms import Lawyer_SearchForm, LitigationTypeForm, BarassociationForm, Lawyer_RegForm
from lawyerFinder.models import Lawyer, LitigationType, Barassociation
from lawyerFinder.models import *
import operator
from random import randint
import json
import re
from django.core.handlers.wsgi import logger
from django.contrib import messages




def redirectHome(re):
    logger.debug("redirect to top page")
    lawyer_searchform = Lawyer_SearchForm()
    litigation_form = LitigationTypeForm()
    barassociation_form = BarassociationForm()

    args = {'lawyer_searchform':lawyer_searchform,
            'litigation_form':litigation_form,
            'barassociation_form':barassociation_form,
            }
    redirect = 'base/index.html'
    
    return render_to_response(
        redirect,
        args,
        context_instance=RequestContext(re)
    )
    
def searchLogic(area_selected, field_selected, gender_selected):
    sep = '========================================================================='
    print sep
    
    SCORE = { 'area':10000,
              'caseNum':1000,
              'gender':100000,
              'premiumType':100,
             }
    start = datetime.datetime.now()
    
    #area_selected = [u'YILAN', u'KEELUNG', u'TAINAN']
    areas = Barassociation.objects.filter(area__in = area_selected)
    
    #field_selected = [u'PC', u'BC', u'BD']
    fields = LitigationType.objects.filter(category__in=field_selected)
    
    print 'area keys = %s, field keys = %s gender = %s' % (area_selected, field_selected, gender_selected)
    
    lawyers = Lawyer.objects.select_related('user').filter(
                          models.Q(lawyermembership__barAssociation=areas) & 
                          models.Q(lawyerspecialty__litigations=fields)).distinct()

    results = []
    #-- generate regex
    areaInput = '('+ "|".join(a for a in area_selected) +')'
    fieldInput = '(\"+[' + "|".join(f for f in field_selected) + ']+\":\"\d+\")'
    genderInput = '(\"['+ "|".join(g for g in gender_selected) +']\")'
    for l in lawyers:
        #-- parse json to dict 
        d = json.loads(str(l))
        #print d['caseNum']['BC']
        
        #-- area regex match for replacing the hit rate 
        pattern = re.compile(areaInput)
        match = pattern.findall(str(l))
        logger.debug('area hitted:%s' % len(match))
        d['area'] = len(match)
        
        #--field regex match for replacing the hit rate 
        pattern = re.compile(fieldInput)
        match = pattern.findall(str(l))
        logger.debug('field hitted:%s' % len(match))
        d['caseNum']=len(match)
        
        #--gender regex match for replacing the value of hitted or not
        pattern = re.compile(genderInput)
        match = pattern.findall(str(l))
        logger.debug('gender hitted:%s' % len(match))
        d['gender']=len(match)
        
        #--calculate total score for ranking
        
        d['rank'] = d['area']*SCORE['area'] + d['caseNum']*SCORE['caseNum'] + d['gender']*SCORE['gender'] + int(d['premiumType'])*SCORE['premiumType']
        # add to the list
        results.append(d)

    #--sort
    newlist = sorted(results, key=operator.itemgetter('rank'), reverse=True)
    
    #--display
    #for i, val in enumerate(newlist):
        #print 'i=%s, val=%s' % (i,val)
        
    end = datetime.datetime.now()
    timeDelta = end-start
    #print timeDelta
    
    return newlist


#@group_required('STAFF')
def home(request):
    args = []
    redirect = ''
    
    if request.method == 'POST':
        litigations = request.POST.getlist('category')
        barass = request.POST.getlist('area')
        gender = request.POST.getlist('gender')

        areas = Barassociation.objects.filter(area__in = barass)
        field = LitigationType.objects.filter(category__in = litigations)
        g_list = [models.Q(gender__contains=x) for x in gender]
        
        
        lawyers = Lawyer.objects.filter(
                        regBarAss__contains=areas).filter(
                        specialty__contains=field).filter(
                        reduce(operator.or_, g_list)).annotate(
                        rank = models.Count('regBarAss', distinct=True)).annotate(
                        field = models.Count('specialty', distinct=True)).order_by(
                        '-rank', '-field', '-premiumType')[0:30]
                        #.values_list('rank', 'field', 'gender', 'premiumType')
        
        #print len(lawyers)
        #for l in lawyers:
        #    print l

        redirect = 'lawyerFinder/_search_results.html'
        args = {'queryed_lawyers':lawyers,
                'areas':areas,
                'field':field,}
        
        
    elif request.method == 'GET': #display main page
        lawyer_searchform = Lawyer_SearchForm()
        litigation_form = LitigationTypeForm()
        barassociation_form = BarassociationForm()
        
        # template name
        redirect = 'base/index.html'
        #redirect = 'lawyerFinder/_index.html'
        args = {'lawyer_searchform':lawyer_searchform,
                'litigation_form':litigation_form,
                'barassociation_form':barassociation_form,
                'title' : 'lawyer',
                }
    
    return render_to_response(
        redirect,
        args,
        context_instance=RequestContext(request)
    )
    
    
    
    
    
def lawyerHome(request, lawyer_id):
    args =''
    
    # retrieve data from DB
    la_info = Lawyer.objects.filter(lawyerNo=lawyer_id)
    if not la_info: 
        logger.debug("No corresponding lawyer!")
        return redirectHome(request)
    
    #if lawyer itself, show full access page
    
    
    #if not, show limited page
    
    
    #prepare for querying from user like email
    #if request.method == 'POST':
    #    pass
    args = {'la_info':la_info}
    
    
    return render_to_response(
        'lawyerFinder/_lawyer_home.html',
        args,
        context_instance=RequestContext(request)
    )
    
    
    
#===============================================================================
def undercons(request):
    args={}
    
    return render_to_response(
        'base/under_cons.html',
        args,
        context_instance=RequestContext(request)
    )
    
def tmp(request):
    args = []
    redirect = ''
    
    if request.method == 'POST':
        pass
        
        
    elif request.method == 'GET': #display main page
        lawyer_searchform = Lawyer_SearchForm()
        litigation_form = LitigationTypeForm()
        barassociation_form = BarassociationForm()
        
        # template name
        redirect = 'base/tmp.html'

        args = {'lawyer_searchform':lawyer_searchform,
                'litigation_form':litigation_form,
                'barassociation_form':barassociation_form,
                'title' : 'lawyer',
                }
    
    return render_to_response(
        redirect,
        args,
        context_instance=RequestContext(request)
    )
    
    