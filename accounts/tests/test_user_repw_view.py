from django.core.urlresolvers import resolve
from django.test import TestCase
from accounts.views import *
from accounts.forms import *
from django.test import TestCase, override_settings




class user_repw_view_test(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser@gmail.com',
                                 email='testuser@gmail.com',
                                 password='1Qa1Qa',
                                 active_flag = False)
        
        
    def test_resolve_to_user_repw_view(self):
        found = resolve('/accounts/repw/')
        self.assertEqual(found.func, user_repw)
        
    def test_user_repw_return_correct_html_when_logged_out(self):
        response = self.client.get("/accounts/repw/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')

    def test_user_repw_return_correct_html_when_logged_in(self):
        #set session value
        u = User.objects.get(username='testuser@gmail.com')
        s = self.client.session
        s['_auth_user_id'] = u.id
        s.save()
        
        response = self.client.get("/accounts/repw", follow=True)
        self.assertEqual(response.status_code, 200)
        
        user_repw_form = User_repw_form()
        #print response.content.decode()
        expected_html = render_to_string('accounts/user_repw.html',
                                         {'user_repw_form':user_repw_form,
                                          'user_email':u.email},
                                         request=response.wsgi_request
                                         )
        #print expected_html
        self.assertEqual(response.content.decode(), expected_html)
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_user_repw_form_is_not_valid_pw_not_identical(self):
        u = User.objects.get(username='testuser@gmail.com')
        s = self.client.session
        s['_auth_user_id'] = u.id
        s.save()
        
        response = self.client.post("/accounts/repw/",
                                    {'oldPassword':'1Qa1Qa',
                                     'newPassword':'2Ws2WS',
                                     'checkPassword':'2Ws2Wss'
                                     })
        self.assertEqual(response.status_code, 200)
        msg = response.context['user_repw_form'].errors
        self.assertTrue('Passwords does not identical.' in str(msg))
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_user_repw_form_is_not_valid_pw_too_short(self):
        u = User.objects.get(username='testuser@gmail.com')
        s = self.client.session
        s['_auth_user_id'] = u.id
        s.save()
        response = self.client.post("/accounts/repw/",
                                    {'oldPassword':'1Qa1Qa',
                                     'newPassword':'2Ws',
                                     'checkPassword':'2Ws'
                                     })
        self.assertEqual(response.status_code, 200)
        msg = response.context['user_repw_form'].errors
        self.assertTrue('Password should be longer than 6 digits' in str(msg))
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_user_repw_form_is_not_valid_pw_no_lower_letter(self):
        u = User.objects.get(username='testuser@gmail.com')
        s = self.client.session
        s['_auth_user_id'] = u.id
        s.save()
        
        response = self.client.post("/accounts/repw/",
                                    {'oldPassword':'1Qa1Qa',
                                     'newPassword':'234WERT',
                                     'checkPassword':'234WERT'
                                     })
        self.assertEqual(response.status_code, 200)
        msg = response.context['user_repw_form'].errors
        self.assertTrue('Password should contain at least 1 number & 1 lower case & 1 upper case & 6 digits combination' in 
                        str(msg).replace("&amp;", "&"))
    
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_user_repw_form_is_not_valid_pw_no_upper_letter(self):
        u = User.objects.get(username='testuser@gmail.com')
        s = self.client.session
        s['_auth_user_id'] = u.id
        s.save()
        
        response = self.client.post("/accounts/repw/",
                                    {'oldPassword':'1Qa1Qa',
                                     'newPassword':'234wert',
                                     'checkPassword':'234wert'
                                     })
        self.assertEqual(response.status_code, 200)
        msg = response.context['user_repw_form'].errors
        self.assertTrue('Password should contain at least 1 number & 1 lower case & 1 upper case & 6 digits combination' in 
                        str(msg).replace("&amp;", "&"))
    
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_user_repw_form_is_not_valid_pw_no_number(self):
        u = User.objects.get(username='testuser@gmail.com')
        s = self.client.session
        s['_auth_user_id'] = u.id
        s.save()
        
        response = self.client.post("/accounts/repw/",
                                    {'oldPassword':'1Qa1Qa',
                                     'newPassword':'WERTwert',
                                     'checkPassword':'WERTwert'
                                     })
        self.assertEqual(response.status_code, 200)
        msg = response.context['user_repw_form'].errors
        self.assertTrue('Password should contain at least 1 number & 1 lower case & 1 upper case & 6 digits combination' in 
                        str(msg).replace("&amp;", "&"))

    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_user_repw_old_pw_not_correct(self):
        u = User.objects.get(username='testuser@gmail.com')
        s = self.client.session
        s['_auth_user_id'] = u.id
        s.save()
        
        response = self.client.post("/accounts/repw/",
                                    {'oldPassword':'1Qa1Qaaaaaaaaaaa',
                                     'newPassword':'WERTwert123',
                                     'checkPassword':'WERTwert123'
                                     })
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.ERROR])
        self.assertEqual('Old PW does not correct', str(messages[0]))
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_user_repw_success(self):
        u = User.objects.get(username='testuser@gmail.com')
        s = self.client.session
        s['_auth_user_id'] = u.id
        s.save()
        
        response = self.client.post("/accounts/repw/",
                                    {'oldPassword':'1Qa1Qa',
                                     'newPassword':'WERTwert123',
                                     'checkPassword':'WERTwert123'
                                     })
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.SUCCESS])
        self.assertEqual('New PW Is Updated', str(messages[0]))

