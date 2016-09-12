from django.core.urlresolvers import resolve
from django.test import TestCase
from accounts.views import *
from django.test import TestCase, override_settings




class repw_view_test(TestCase):
    def setUp(self):
        pass
    
    def test_resolve_to_repw_view(self):
        found = resolve('/accounts/')
        self.assertEqual(found.func, repw_view)
    
    def test_repw_return_correct_html(self):
        response = self.client.get("/accounts/")
        self.assertEqual(response.status_code, 200)
        
        expected_html = render_to_string('accounts/_base.html',
                                         request=response.wsgi_request)
        
        self.assertEqual(response.content.decode(), expected_html)
    
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_repw_post_form_validation(self):
        response = self.client.post("/accounts/",
                                    {'username':'',
                                     'type':'REPW'})
        
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.ERROR])
        self.assertEqual('Please Input Email Account', str(messages[0]))
        
    '''
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_repw_post_repassword_and_active_request(self):
        u = User.objects.create_user(username='dragonbrucelee@gmail.com',
                                 email='dragonbrucelee',
                                 password='1Qa1Qa',
                                 active_flag=True)
        
        response = self.client.post("/accounts/",
                                    {'username':'dragonbrucelee@gmail.com',
                                     'type':'REPW'})
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.SUCCESS])
        self.assertEqual('Please check your new pw in your email account', str(messages[0]))
        
    '''
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_repw_post_repassword_and_unactive_request(self):
        u = User.objects.create_user(username='dragonbrucelee@gmail.com',
                                 email='dragonbrucelee',
                                 password='1Qa1Qa',
                                 active_flag=False)
        
        response = self.client.post("/accounts/",
                                    {'username':'dragonbrucelee@gmail.com',
                                     'type':'REPW'})
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.WARNING])
        self.assertEqual('This ID has not been activated. Please check your mailbox', str(messages[0]))
        
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_repw_post_repassword_unregistered_account(self):
        u = User.objects.create_user(username='dragonbrucelee@gmail.com',
                                 email='dragonbrucelee',
                                 password='1Qa1Qa',
                                 active_flag=True)
        
        response = self.client.post("/accounts/",
                                    {'username':'doublenunchakus@gmail.com',
                                     'type':'REPW'})
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.ERROR])
        self.assertEqual('This Email has not been registered', str(messages[0]))
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_repw_post_reconfirm_already_activated(self):
        u = User.objects.create_user(username='dragonbrucelee@gmail.com',
                                 email='dragonbrucelee',
                                 password='1Qa1Qa',
                                 active_flag=True)
        
        response = self.client.post("/accounts/",
                                    {'username':'dragonbrucelee@gmail.com',
                                     'type':'RECO'})
        
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.WARNING])
        self.assertEqual('This ID has been activated.', str(messages[0]))
        
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_repw_post_reconfirm_not_activated(self):
        u = User.objects.create_user(username='dragonbrucelee@gmail.com',
                                 email='dragonbrucelee',
                                 password='1Qa1Qa',
                                 active_flag=False)
        
        response = self.client.post("/accounts/",
                                    {'username':'dragonbrucelee@gmail.com',
                                     'type':'RECO'})
        
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.SUCCESS])
        self.assertEqual('Please Check The Confirmation Mail In Your Mailbox', str(messages[0]))
        
        
        
        
        
        
        
    
    
    