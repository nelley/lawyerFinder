from django.shortcuts import render, redirect, render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
import logging
import datetime
from accounts.cus_decorators import group_required
from lawyerFinder.forms import *
from lawyerFinder.models import Lawyer, LitigationType, Barassociation
from lawyerFinder.models import *
import operator
from random import randint
import json
import re
from django.http import HttpResponse
from django.core.handlers.wsgi import logger
from django.db import IntegrityError, transaction
from django.contrib.messages.api import success

from bootstrap3.forms import render_form




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
    
    
    
    
    
def lawyerHome(request, law_id):
    args =''
    
    if request.method=='POST' and request.is_ajax():
        data = {} # for response
        
        if request.method == 'POST' and 'service_edit' in request.POST:
            logger.debug("Service Edit's Ajax start")
            submitted_form = Lawyer_infosForm(request.POST)
            if submitted_form.is_valid():
                commitedContent = updateLawyerInfo(request, submitted_form)
                
                data['result'] = 'success'
                data['message'] = 'Upload Completed'
                data['contents'] = commitedContent
                data['type'] = request.POST['type']
                
            else:
                data['result'] = 'danger'
                data['message'] = 'Upload Failed'
                logger.debug("Upload Failed!!")
                
            return HttpResponse(json.dumps(data), content_type="application/json")
        
        elif(request.method == 'POST' and 'profile_fetch' in request.POST):
            logger.debug("Profile Fetch's Ajax start")
            lawyerObj = getLawyerInfo(request)
            
            
            lawyer_regform = Lawyer_RegForm(instance=lawyerObj, lawyer=lawyerObj)
            #print render_form(lawyer_regform)
            
            if lawyerObj:
                return HttpResponse(render_form(lawyer_regform))
                #return HttpResponse(lawyerObj.print_json(), content_type="application/json")
            else:
                data['result'] = 'danger'
                data['message'] = 'Upload Failed'
                logger.debug("Profile Fetch Failed!!")
                return HttpResponse(json.dumps(data), content_type="application/json")
        
        else:
            return HttpResponse('ajax get call')
    
    elif request.method == 'POST':
        logger.debug("POST ONLY!")
        return HttpResponse('hello world')
        
    else:
        logger.debug("GET ONLY!")
        # retrieve data from DB
        try:
            law_selected = Lawyer.objects.get(lawyerNo=law_id)
            law_iform = Lawyer_infosForm();#init ckeditor
            law_infos = Lawyer_infos.objects.get(lawyer_id=law_selected)#retrieve all info from lawyer_infos table(created when initing lawyer)
            if law_infos:
                #lawyer_regform = Lawyer_RegForm(instance=law_selected, lawyer=law_selected)
                #print law_selected
                args = {'law_selected':law_selected,
                        'law_iform':law_iform,
                        'law_infos':law_infos,}
                        #'lawyer_regform':lawyer_regform}
                
                logger.debug("Lawyer Info rendered!")
                return render_to_response('lawyerFinder/_lawyer_home.html',
                                          args,
                                          context_instance=RequestContext(request)
                                          )
            
        except Lawyer.DoesNotExist:
            logger.debug("No corresponding lawyer!")
            return redirectHome(request)
    
    
    logger.debug("default return")
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
        lawyer_infosForm = Lawyer_infosForm(request.POST)
        l = Lawyer.objects.get(lawyerNo='13000')
        
        if lawyer_infosForm.is_valid():
            input = lawyer_infosForm.cleaned_data['basic']
            Lawyer_infos.objects.create(lawyer=l, basic=input)
            
            
            
        lawyer_infosForm = Lawyer_infosForm()
        
        
    elif request.method == 'GET': #display main page
        lawyer_infosForm = Lawyer_infosForm()
        lawyer_input = Lawyer_infos.objects.get(lawyer_id='205')
        
    # template name
    redirect = 'base/tmp.html'
    args = {'testform' : lawyer_infosForm,
            'lawyer_input' : lawyer_input,
            }
    
    return render_to_response(
        redirect,
        args,
        context_instance=RequestContext(request)
    )
    

def updateLawyerInfo(res, form):
    logger.debug("updateLawyerInfo Start")
    
    newInfos = form.cleaned_data['basic']
    type = res.POST['type']
    userid = res.session['_auth_user_id']
    try:
        l = Lawyer.objects.get(user_id= userid)
        lawinfo = Lawyer_infos.objects.get(lawyer_id = l.user_id)
        
        if type == '1': #basic
            lawinfo.basic = newInfos
        elif type == '2': #strongFields
            lawinfo.strongFields = newInfos
        elif type =='3': # finishedCases
            lawinfo.finishedCases = newInfos
        elif type == '4': #feeStd
            lawinfo.feeStd = newInfos
        elif type == '5': #companyInfos
            lawinfo.companyInfos= newInfos
        else:
            pass
        
        lawinfo.save()
        logger.debug("db updating completed")
        
    except Lawyer.DoesNotExist:
        return False
    
    return newInfos
    
def getLawyerInfo(res):
    userid = res.session['_auth_user_id']
    try:
        l = Lawyer.objects.get(user_id= userid)
    except Lawyer.DoesNotExist:
        return False
    return l
#========================================================================
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    
    items = Item.objects.all()
    
    return render(request, 'unittest/test.html', {'items': items})

def view_list(request):
    items = Item.objects.all()
    return render(request, 'unittest/test.html', {'items': items})






