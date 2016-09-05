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
from accounts.forms import *
from common.utilities import ajax_session_check
from lawyerFinder.settings import *
from PIL import Image
from django.utils.translation import ugettext_lazy as _
from common.utilities import *

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
        #image_path = MEDIA_ROOT + lawyers.photos
        
        args = {'queryed_lawyers':lawyers,
                #'img_path':image_path,
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
    
    
    
    
def service_rule(request):
    sr = WebStaticContents.objects.get(key='SERVICE_RULE')
    args={
          'service_rules':sr,
          }
    
    return render_to_response(
        'common/site_service_rule.html',
        args,
        context_instance=RequestContext(request)
    )

#for lawyer access
@transaction.atomic
def lawyerHomeMyPage(request, law_id):
    logger.debug('lawyerHome access for lawyer')
    args = ''
    if request.method=='POST' and request.is_ajax():
        data = {} # for response
        
        #check session timeout when ajax call
        if(not ajax_session_check(request)):
            data = {
                    'result':'timeout',
                    'title':unicode(_('Session Timeout')),
                    'message':unicode(_('Your Session Is Timeout')),
                    'home_url':SITE_URL,
                    }
            
            logger.debug("session timeout")
            return HttpResponse(json.dumps(data), content_type="application/json")
        
        if request.method == 'POST' and 'service_edit' in request.POST:
            logger.debug("Service Edit's Ajax start")
            submitted_form = Lawyer_infosForm(request.POST)
            if submitted_form.is_valid():
                commitedContent = updateLawyerInfo(request, submitted_form)
                
                data = {
                        'result':'success',
                        'message':unicode(_('Edit Successed')),
                        'contents':commitedContent,
                        'type':request.POST['type']
                        }
                
            else:
                data = {
                        'result':'danger',
                        'message':unicode(_('Process Failed')),
                        }
                logger.debug("Upload Failed!!")
                
            return HttpResponse(json.dumps(data), content_type="application/json")
        
        elif(request.method == 'POST' and 'profile_fetch' in request.POST):
            logger.debug("Profile Fetch's Ajax start")
            lawyerObj = getLawyerInfo(request)
            
            lawyer_regform = Lawyer_RegForm(request, instance=lawyerObj, lawyer=lawyerObj)
            
            u = User.objects.get(id=lawyerObj.user_id)
            lawyer_nameform = Lawyer_Nameform(instance=u)
            
            if lawyerObj:
                #return HttpResponse(render_form(lawyer_regform))
                return HttpResponse(render_form(lawyer_nameform) + render_form(lawyer_regform))
            else:
                data['result'] = 'danger'
                data['message'] = 'Upload Failed'
                logger.debug("Profile Fetch Failed!!")
                return HttpResponse(json.dumps(data), content_type="application/json")
        
        elif(request.method == 'POST' and 'editCommit' in request.POST):
            logger.debug("Profile edit commit Ajax start")
            submittedForm = json.loads(request.POST['form'])
            objForInit, userObj = rearrangeForm(submittedForm)
            
            lawyer_regform_edit = Lawyer_RegForm(request, objForInit)
            lawyer_nameform_edit = Lawyer_Nameform(userObj)

            if lawyer_regform_edit.is_valid() and lawyer_nameform_edit.is_valid():
                updateLawyerProfile(request, lawyer_regform_edit)
                updateUserProfile(request, lawyer_nameform_edit)
                
                data = {
                        'result':'success',
                        'message':unicode(_('Edit Successed')),
                        'first_name':userObj['first_name'],
                        'last_name':userObj['last_name'],
                        
                        }
                
                return HttpResponse(json.dumps(data), content_type="application/json")
            
            else:
                logger.debug("Validation Failed")
                return HttpResponse(render_form(lawyer_nameform_edit) + 
                                    render_form(lawyer_regform_edit))
            
        elif(request.method == 'POST' and 'photo_fetch' in request.POST):
            lawyer_photoform = Lawyer_photoForm()
            
            return HttpResponse(render_form(lawyer_photoform))
        
        elif(request.method == 'POST' and 'photo_edit_commit' in request.POST):
            if 'imgFile' in request.FILES:
                try:
                    with transaction.atomic():
                        imageFileBuf = request.FILES['imgFile']
                        PIL_image = Image.open(imageFileBuf)
                        tmpL = getLawyerInfo(request)
                        
                        thumbnail_save_path = MEDIA_ROOT + '/' + tmpL.lawyerNo + '/thumbnail/'
                        image_save_path = MEDIA_ROOT + '/' + tmpL.lawyerNo + '/image/'
                        
                        logger.debug('thumbnail store path = %s' % thumbnail_save_path)
                        logger.debug('original image store path = %s' % image_save_path)
                        
                        #folder check for thumbnail
                        #if not os.path.exists(thumbnail_save_path):
                        #    os.makedirs(thumbnail_save_path)
                            
                        #folder check for original image
                        if not os.path.exists(image_save_path):
                            os.makedirs(image_save_path)
                            
                        #check width & height before saving as thumbnail
                        #w,h = PIL_image.size
                        #if w > PROFILE_IMG_WIDTH or h > PROFILE_IMG_HEIGHT:
                        #    PIL_thumbnail = PIL_image.resize((PROFILE_IMG_WIDTH, PROFILE_IMG_WIDTH))
                        #    PIL_thumbnail.save(thumbnail_save_path + imageFileBuf.name.lower(), 'JPEG')
                        #else:
                        #    PIL_image.save(thumbnail_save_path + imageFileBuf.name.lower(), 'JPEG')
                        
                        #save to the folder categoried by lawyer number
                        PIL_image.save(image_save_path + imageFileBuf.name.lower(), 'JPEG')
                        
                        logger.debug('thumbnail & image saving completed!')
                        
                        img_db_path = tmpL.lawyerNo + '/image/' + imageFileBuf.name.lower()
                        #update data in DB
                        tmpL.photos = img_db_path
                        #tmpL.thumbnail = '/' + tmpL.lawyerNo + '/thumbnail/' + imageFileBuf.name.lower()
                        tmpL.save()
                        logger.debug('thumbnail & image path saving to DB completed!')
                        
                        data = { 'result':'Success',
                                 'title':unicode(_('Edit Successed')),
                                 'message':unicode(_('Your Profile Image Is Changed')),
                                 'img_url':MEDIA_URL + img_db_path,
                                }
                        
                        return HttpResponse(json.dumps(data), content_type="application/json")
                    
                except Exception as e:
                    print e
                    data = {
                        'result':'System Error',
                        'title':unicode(_('Selected file is not an image')),
                        'message':unicode(_('Please select an image file')),
                        }
                    return HttpResponse(json.dumps(data), content_type="application/json")
                    logger.debug('%s (%s)' % (e.message, type(e)))
                
                
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                logger.debug('there is no image file in the request')
                data = {
                        'result':'Failed',
                        'title':unicode(_('Process Failed')),
                        'message':unicode(_('Please Select An Image File')),
                        }
                
                return HttpResponse(json.dumps(data), content_type="application/json")
            
        else:
            logger.debug('ajax GET call comes')
            return HttpResponse('ajax get call LA')
    
    elif request.method == 'POST':
        logger.debug("POST ONLY!")
        return HttpResponse('hello world')
        
    else:
        logger.debug("GET(Only) request from lawyerHome")
        # retrieve data from DB
        try:
            law_selected = Lawyer.objects.get(lawyerNo=law_id)
            law_iform = Lawyer_infosForm();#init ckeditor
            law_infos = Lawyer_infos.objects.get(lawyer_id=law_selected)#retrieve all info from lawyer_infos table(created when initing lawyer)
            ajax_path = '/lawyerHome/mypage/' + law_id
            if law_infos:
                args = {'law_selected':law_selected,
                        'law_iform':law_iform,
                        'law_infos':law_infos,
                        'img_path':law_selected.photos,
                        'ajax_path':ajax_path,}
                
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
    


#for guest/ordinary user access
@transaction.atomic
def lawyerHome(request, law_id):
    logger.debug('lawyerHome access for ordinary user/guest')
    args =''
    
    if request.method=='POST' and request.is_ajax():
        data = {} # for response
        
        if request.method == 'POST' and 'mail_consult_fetch' in request.POST:
            user_inquiry_form = User_Inquiry_Form()
            return HttpResponse(render_form(user_inquiry_form))
        
        elif request.method == 'POST' and 'send_mail' in request.POST:
            sentForm = json.loads(request.POST['form'])
            
            sentFormObj = rearrangeSentForm(sentForm)
            user_inquiry_form_edit = User_Inquiry_Form(sentFormObj)
            
            if user_inquiry_form_edit.is_valid():
                l = Lawyer.objects.get(lawyerNo = request.build_absolute_uri().split("/")[-1])
                u = User.objects.get(id = l.user_id)
                
                # translate incidentType & incidentPlace
                sentFormObj['incidentPlace'] = Barassociation.objects.get(area=''.join(sentFormObj['incidentPlace'])).area_cn
                sentFormObj['incidentType'] = LitigationType.objects.get(category=''.join(sentFormObj['incidentType'])).category_cn
                
                userInquirySender(u.email, sentFormObj)

                '''
                try:
                    #retrieve user id & lawyer id
                    user_inquiry = user_inquiry_form_edit.save(commit=False)
                    user_inquiry.lawyerNo = request.build_absolute_uri().split("/")[-1]
                    
                    user_inquiry.incidentType = user_inquiry_form_edit.cleaned_data['incidentType']
                    user_inquiry.incidentPlace = user_inquiry_form_edit.cleaned_data['incidentPlace']
                    
                    if '_auth_user_id' in request.session:
                        user_inquiry.user_id = request.session['_auth_user_id']
                    else:
                        user_inquiry.user = None
                        
                    user_inquiry.save()
                except IntegrityError:
                    return False
                '''
                #send mail
                #l = Lawyer.objects.get(lawyerNo=request.build_absolute_uri().split("/")[-1])
                
                
                data = {
                        'result':'success',
                        'title':unicode(_('Mail sent')),
                        'message':unicode(_('Mail sent')),
                        }
            else:
                logger.debug("Validation Failed")
                return HttpResponse(render_form(user_inquiry_form_edit))
            
            return HttpResponse(json.dumps(data), content_type="application/json")
        
        else:
            
            logger.debug('ajax GET call comes')
            return HttpResponse('ajax get call')
    
    elif request.method == 'POST':
        logger.debug("POST ONLY!")
        return HttpResponse('hello world')
        
    else:
        logger.debug("GET(Only) request from lawyerHome")
        # retrieve data from DB
        try:
            law_selected = Lawyer.objects.get(lawyerNo=law_id)
            law_iform = Lawyer_infosForm();#init ckeditor
            law_infos = Lawyer_infos.objects.get(lawyer_id=law_selected)#retrieve all info from lawyer_infos table(created when initing lawyer)
            ajax_path = '/lawyerHome/' + law_id 
            if law_infos:
                args = {'law_selected':law_selected,
                        'law_iform':law_iform,
                        'law_infos':law_infos,
                        'img_path':law_selected.photos,
                        'ajax_path':ajax_path}
                
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
    

def updateUserProfile(req, userForm):
    logger.debug("updateUserProfile")
    userid = req.session['_auth_user_id']
    
    try:
        uu = User.objects.get(id=userid)
        uu.first_name = userForm.cleaned_data['first_name']
        uu.last_name = userForm.cleaned_data['last_name']
        uu.save()
        
    except IntegrityError:
        return False
    
def updateLawyerProfile(req, tmpForm):
    logger.debug("updateLawyerProfile Start")
    userid = req.session['_auth_user_id']

    try:
        l = Lawyer.objects.get(user_id= userid)
        l.lawyerNo = tmpForm.cleaned_data['lawyerNo']
        l.gender = tmpForm.cleaned_data['gender']
        l.companyAddress = tmpForm.cleaned_data['companyAddress']
        l.careerYear = tmpForm.cleaned_data['careerYear']
        l.phone_number = tmpForm.cleaned_data['phone_number']

        LawyerMembership.objects.filter(lawyerNo=userid).delete()
        areas = Barassociation.objects.filter(area__in = tmpForm.cleaned_data['regBarAss'])
        LawyerMembership.objects.create_in_bulk(l, areas)
        
        LawyerSpecialty.objects.filter(lawyerNo=l.user_id).delete()
        fields = LitigationType.objects.filter(category__in = tmpForm.cleaned_data['specialty'])
        LawyerSpecialty.objects.create_in_bulk(l, fields)
        
        l.save()
        
    except IntegrityError:
        return False
        
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


'''
    rebuild json data to 
'''
def rearrangeSentForm(tmpForm):
    formObject={}
    tmp_incidentPlace = []
    tmp_incidentType = []
    
    for i in tmpForm:
        if i['name'] == 'inquiryTitle':
            formObject['inquiryTitle'] = i['value']
        elif i['name'] == 'inquiryContents':
            formObject['inquiryContents'] = i['value']
        elif i['name'] == 'email':
            formObject['email'] = i['value']
        elif i['name'] == 'phoneNumber':
            formObject['phoneNumber'] = i['value']
        elif 'incidentPlace' in i['name']:
            tmp_incidentPlace.append(i['value'])
        elif 'incidentType' in i['name']:
            tmp_incidentType.append(i['value'])
            
        formObject['incidentPlace'] = tmp_incidentPlace
        formObject['incidentType'] = tmp_incidentType
    
    return formObject

'''
    rebuild json data to reg_form object's format
'''
def rearrangeForm(tmpForm):
    formObject={}
    tmp_regBarAss = []
    tmp_specialty = []

    for i in tmpForm:
        if i['name'] == 'lawyerNo':
            formObject['lawyerNo'] = i['value']
        elif i['name'] == 'careerYear':
            formObject['careerYear'] = i['value']
        elif i['name'] == 'gender':
            formObject['gender'] = i['value']
        elif i['name'] == 'phone_number':
            formObject['phone_number'] = i['value']
        elif i['name'] == 'companyAddress':
            formObject['companyAddress'] = i['value']
        elif 'regBarAss' in i['name'] :
            tmp_regBarAss.append(i['value'])
        elif 'specialty' in i['name']:
            tmp_specialty.append(i['value'])
        elif i['name'] in 'first_name':
            userObject['first_name'] = i['value']
        elif i['name'] in 'last_name':
            userObject['last_name'] = i['value']
            
    formObject['regBarAss'] = tmp_regBarAss
    formObject['specialty'] = tmp_specialty
    
    return (formObject, userObject)
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






