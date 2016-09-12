from django.core.urlresolvers import resolve
from django.test import TestCase
from lawyerFinder.views import *
from common.testUtil import *
from django.template.loader import render_to_string
from django.test import TestCase, override_settings

class lawyerHome_test(TestCase):
    
    def setUp(self):
        pass
    
    def test_resolve_to_correct_lawyerHome_view(self):
        found = resolve('/lawyerHome/13001')
        self.assertEqual(found.func, lawyerHome)

    def test_resolve_to_mistake_lawyerHome_view(self):
        found = resolve('/lawyerHome/13001')
        self.assertEqual(found.func, lawyerHome)

    def test_lawyerHome_with_ajax_mail_consult_fetch(self):
        response = self.client.post("/lawyerHome/13001",
                                    {'mail_consult_fetch':'action'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        
        user_inquiry_form = User_Inquiry_Form()
        self.assertEqual(response.content.decode(), render_form(user_inquiry_form))
        
    
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_lawyerHome_with_ajax_send_mail_success(self):
        u = User.objects.create_user(username='dragonbrucelee@gmail.com',
                                 email='dragonbrucelee@gmail.com',
                                 password='1Qa1Qa',
                                 active_flag = True)
        
        l = Lawyer(user=u, lawyerNo='13001', 
                   gender=Lawyer.GENDER[randint(0,1)][0], 
                   premiumType=Lawyer.PREMIUM[randint(0,3)][0], 
                   careerYear=randint(0,20))
        l.save()
        
        jsonStr = '[{"name":"inquiryTitle", "value":"test_lawyerHome"},\
                    {"name":"incidentPlace", "value":"HUALIEN"},\
                    {"name":"incidentType", "value":"IP"},\
                    {"name":"inquiryContents", "value":"test_lawyerHome_with_ajax_send_mail contents"},\
                    {"name":"email", "value":"dragonbrucelee@gmail.com"},\
                    {"name":"phoneNumber", "value":"0905-239-285"}]'
        
        response = self.client.post("/lawyerHome/13001",
                                    {'send_mail':'action',
                                     'form':jsonStr},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        json_string = response.content
        data = json.loads(json_string)
        
        #check db
        ui = UserInquiry.objects.get(email=u.username)
        self.assertEqual('test_lawyerHome_with_ajax_send_mail contents', ui.inquiryContents)
        
        #check msg
        self.assertEqual('success', data['result'])
        self.assertEqual('Mail sent', data['title'])
        self.assertEqual('Mail sent', data['message'])
        
    
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_lawyerHome_with_ajax_send_mail_validation_fail(self):
        u = User.objects.create_user(username='dragonbrucelee@gmail.com',
                                 email='dragonbrucelee@gmail.com',
                                 password='1Qa1Qa',
                                 active_flag = True)
        
        l = Lawyer(user=u, lawyerNo='13001', 
                   gender=Lawyer.GENDER[randint(0,1)][0], 
                   premiumType=Lawyer.PREMIUM[randint(0,3)][0], 
                   careerYear=randint(0,20))
        l.save()
        
        jsonStr = '[{"name":"inquiryTitle", "value":"test_lawyerHome+with_ajax_send_mail"},\
                    {"name":"incidentPlace", "value":"HUALIEN"},\
                    {"name":"incidentType", "value":"IP"},\
                    {"name":"inquiryContents", "value":"test_lawyerHome_with_ajax_send_mail contents"},\
                    {"name":"email", "value":"dragonbrucelee@gmail.com"},\
                    {"name":"phoneNumber", "value":"0905-239-285"}]'
        
        response = self.client.post("/lawyerHome/13001",
                                    {'send_mail':'action',
                                     'form':jsonStr},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Ensure this value has at most 20 characters (it has 35).' in str(response.content.decode()))
    
        
    def test_lawyerHome_with_ajax_fetch_phoneNumber(self):
        u = User.objects.create_user(username='dragonbrucelee@gmail.com',
                                 email='dragonbrucelee@gmail.com',
                                 password='1Qa1Qa',
                                 active_flag = True)
        
        l = Lawyer(user=u, lawyerNo='13001', 
                   phoneNumber='0905-239-285',
                   gender=Lawyer.GENDER[randint(0,1)][0], 
                   premiumType=Lawyer.PREMIUM[randint(0,3)][0], 
                   careerYear=randint(0,20))
        l.save()
        
        response = self.client.post("/lawyerHome/13001",
                                    {'fetch_phoneNumber':'action'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json_string = response.content
        data = json.loads(json_string)
        self.assertEqual('success', data['result'])
        self.assertEqual('0905-239-285', data['phone_number'])
    
    def test_lawyerHome_with_ajax_fetch_phoneNumber_no_phoneNumber(self):
        userGenerator()
        response = self.client.post("/lawyerHome/13001",
                                    {'fetch_phoneNumber':'action'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        json_string = response.content
        data = json.loads(json_string)
        
        self.assertEqual('Failed', data['result'])
        self.assertEqual('No Phone Number Registered', data['phone_number'])
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_lawyerHome_with_ajax_session_timeout(self):
        response = self.client.post("/lawyerHome/13001",
                                    {'service_edit':'action'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        json_string = response.content
        data = json.loads(json_string)
        
        self.assertEqual('timeout', data['result'])
        self.assertEqual('Session Timeout', data['title'])
        self.assertEqual('Your Session Is Timeout', data['message'])
        
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_lawyerHome_with_ajax_service_edit_fail(self):
        connect_under_login_lawyer(self, 'dragonbrucelee@gmail.com', '1Qa1Qa', '13001')
                                 
        response = self.client.post("/lawyerHome/13001",
                                    {'service_edit':'action'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        
        json_string = response.content
        data = json.loads(json_string)
        
        self.assertEqual('danger', data['result'])
        self.assertEqual('Process Failed', data['message'])
        
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_lawyerHome_with_ajax_service_edit_success_in_basic_field(self):
        ckeditor_input = '<h4>Your Service</h4><p>Please Edit Your Service</p>'
        connect_under_login_lawyer(self, 'dragonbrucelee@gmail.com', '1Qa1Qa', '13001', ckeditor_input)
        
        response = self.client.post("/lawyerHome/13001",
                                    {'service_edit':'action',
                                     'basic':ckeditor_input,
                                     'type':1},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        
        json_string = response.content
        data = json.loads(json_string)
        
        self.assertEqual('success', data['result'])
        self.assertEqual('Edit Successed', data['message'])
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_lawyerHome_with_ajax_profile_fetch(self):
        connect_under_login_lawyer(self, 
                                   loginId='dragonbrucelee@gmail.com', 
                                   loginPW='1Qa1Qa', 
                                   lawyerNo='13001')
        
        response = self.client.post("/lawyerHome/13001",
                                    {'profile_fetch':'action'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        
        lawyerObj = is_lawyer(response.wsgi_request)
        u = User.objects.get(username='dragonbrucelee@gmail.com')
        
        lawyer_regform = Lawyer_RegForm(response.wsgi_request, instance=lawyerObj, lawyer=lawyerObj)
        lawyer_nameform = Lawyer_Nameform(instance=u)
        
        self.assertEqual(response.content.decode(),render_form(lawyer_nameform)+render_form(lawyer_regform))
        
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_lawyerHome_with_ajax_editCommit(self):
        jsonStr='[{"name":"first_name", "value":"test"},\
                  {"name":"last_name", "value":"tarou"},\
                  {"name":"lawyerNo", "value":"13001"},\
                  {"name":"gender", "value":"M"},\
                  {"name":"careerYear", "value":"2"},\
                  {"name":"companyAddress", "value":"test address"},\
                  {"name":"phoneNumber", "value":"0911-208-099"},\
                  {"name":"id_regBarAss", "value":"NANTOU"},\
                  {"name":"id_specialty", "value":"FT"}]'
        
        connect_under_login_lawyer(self, 
                                   loginId='dragonbrucelee@gmail.com', 
                                   loginPW='1Qa1Qa', 
                                   lawyerNo='13001')
        
        response = self.client.post("/lawyerHome/13001",
                                    {'editCommit':'action',
                                     'form':jsonStr},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        
        json_string = response.content
        data = json.loads(json_string)
        
        self.assertEqual('success', data['result'])
        self.assertEqual('Edit Successed', data['title'])
        self.assertEqual('Your Profile Has Been Updated', data['message'])
        
    def test_lawyerHome_with_ajax_photo_fetch(self):
        connect_under_login_lawyer(self, 
                                   loginId='dragonbrucelee@gmail.com', 
                                   loginPW='1Qa1Qa', 
                                   lawyerNo='13001')
        
        response = self.client.post("/lawyerHome/13001",
                                    {'photo_fetch':'action'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        
        lawyer_photoform = Lawyer_photoForm()
        
        self.assertEqual(response.content.decode(), render_form(lawyer_photoform))
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_lawyerHome_with_ajax_photo_commit_success(self):
        connect_under_login_lawyer(self, 
                                   loginId='dragonbrucelee@gmail.com', 
                                   loginPW='1Qa1Qa', 
                                   lawyerNo='13001')
        
        with open('/home/nelley/dj_pj_NL/lawyerFinder/lawyerFinder/tests/test_material/img_test.jpg') as fp:
            response = self.client.post("/lawyerHome/13001",
                                        {'photo_edit_commit':'action',
                                         'imgFile':fp},
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            
        self.assertEqual(response.status_code, 200)
        
        json_string = response.content
        data = json.loads(json_string)
        
        self.assertEqual('Success', data['result'])
        self.assertEqual('Edit Successed', data['title'])
        self.assertEqual('Your Profile Image Is Changed', data['message'])
        
        
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_lawyerHome_with_ajax_photo_commit_pdf_fail(self):
        connect_under_login_lawyer(self, 
                                   loginId='dragonbrucelee@gmail.com', 
                                   loginPW='1Qa1Qa', 
                                   lawyerNo='13001')
        
        with open('/home/nelley/dj_pj_NL/lawyerFinder/lawyerFinder/tests/test_material/pdf-test.pdf') as fp:
            response = self.client.post("/lawyerHome/13001",
                                        {'photo_edit_commit':'action',
                                         'imgFile':fp},
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
                
        self.assertEqual(response.status_code, 200)
        
        json_string = response.content
        data = json.loads(json_string)
        
        self.assertEqual('System Error', data['result'])
        self.assertEqual('Selected file is not an image', data['title'])
        self.assertEqual('Please select an image file', data['message'])
        
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_lawyerHome_with_ajax_photo_commit_no_file(self):
        connect_under_login_lawyer(self, 
                                   loginId='dragonbrucelee@gmail.com', 
                                   loginPW='1Qa1Qa', 
                                   lawyerNo='13001')
        
        response = self.client.post("/lawyerHome/13001",
                                    {'photo_edit_commit':'action'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            
        self.assertEqual(response.status_code, 200)
        
        json_string = response.content
        data = json.loads(json_string)
        
        self.assertEqual('Failed', data['result'])
        self.assertEqual('Process Failed', data['title'])
        self.assertEqual('Please Select An Image File', data['message'])
        
    def test_lawyerHome_with_ajax_call_unknown(self):
        connect_under_login_lawyer(self, 
                                   loginId='dragonbrucelee@gmail.com', 
                                   loginPW='1Qa1Qa', 
                                   lawyerNo='13001')
        
        response = self.client.post("/lawyerHome/13001",
                                    {'unknown':'action'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        
        json_string = response.content
        data = json.loads(json_string)
        
        self.assertEqual('Failed', data['result'])
        self.assertEqual('Process Unknown', data['title'])
        self.assertEqual('Process Unknown', data['message'])
        
        
        
        
    def test_lawyerHome_with_post_call_only(self):
        connect_under_login_lawyer(self, 
                                   loginId='dragonbrucelee@gmail.com', 
                                   loginPW='1Qa1Qa', 
                                   lawyerNo='13001')
        
        response = self.client.post("/lawyerHome/13001")
        
        self.assertEqual(response.status_code, 200)
        