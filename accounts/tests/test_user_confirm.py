from django.core.urlresolvers import resolve
from django.test import TestCase
from accounts.views import *
from django.http import HttpRequest
from django.template.loader import render_to_string
from lawyerFinder.models import *
from accounts.models import *
from django.utils.translation import ugettext_lazy as _
from lawyerFinder.settings import *
from django.test import TestCase, override_settings
from django.test import Client
from common.utilities import *
from datetime import datetime, timedelta


# Create your tests here.
class user_confirm_test(TestCase):
    #fixtures = [FIXTURE_DIRS + 'initial_data.json']
    
    def setUp(self):
        self.email1='testuser@gmail.com'
        self.password1='1Qa1Qa'
        
        self.email2='test2user@gmail.com'
        self.password2='1Qa1Qa'
        
        User.objects.create_user(username=self.email1,
                                 email=self.email1,
                                 password=self.password1,
                                 active_flag = False)
        
        User.objects.create_user(username=self.email2,
                                 email=self.email2,
                                 password=self.password2,
                                 active_flag = False)
        
        self.token1 = gen_tokens(User.objects.get(username=self.email1).email)
        self.token2 = gen_tokens(User.objects.get(username=self.email2).email)
        
        RegistTokens.objects.create(email=self.email1,
                                    registkey=self.token1)
        
        RegistTokens.objects.create(email=self.email2,
                                    registkey=self.token2,
                                    created_at=datetime.now() + timedelta(hours=-9))
    
    def test_resolves_to_user_confirm_view(self):
        found = resolve('/accounts/registConfirm/' + self.token1)
        self.assertEqual(found.func, user_confirm)
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_user_confirmation_with_correct_token(self):
        # use follow=True to follow redirect 
        response = self.client.post("/accounts/registConfirm/" + self.token1, follow=True)
        self.assertRedirects(response, '/')
        
        messages = list(response.context['messages'])
        
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.SUCCESS])
        self.assertEqual('Account activated', str(messages[0]))
    
    
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_user_confirmation_over_2_hoursx(self):
        response = self.client.post("/accounts/registConfirm/" + self.token2, follow=True)
        self.assertRedirects(response, '/')
        
        messages = list(response.context['messages'])
        
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.ERROR])
        self.assertEqual('Invalid register key due to exceed time limitation', 
                        str(messages[0]))
        
    def test_user_confirmation_with_fake_token(self):
        response = self.client.post("/accounts/registConfirm/" + 'abcdefg')
        self.assertRedirects(response, '/')
        
        
    '''
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_input_pw_no_lower_letter(self):
        response = self.client.post("/accounts/userregister/",
                                     {'username':'dragonbrucelee@gmail.com',
                                      'password':'12345TT',
                                      'checkpassword':'12345TT',
                                      'siterule':'YES'
                                      }
                                    )
        
        self.assertEqual(response.status_code, 200)
        
        messages = list(response.context['messages'])
        
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.ERROR])
        self.assertEqual('Password should contain at least 1 number & 1 lower case & 1 upper case & 6 digits combination', 
                        str(messages[0]))
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_input_pw_no_upper_letter(self):
        response = self.client.post("/accounts/userregister/",
                                     {'username':'dragonbrucelee@gmail.com',
                                      'password':'12345tt',
                                      'checkpassword':'12345tt',
                                      'siterule':'YES'
                                      }
                                    )
        
        self.assertEqual(response.status_code, 200)
        
        messages = list(response.context['messages'])
        
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.ERROR])
        self.assertEqual('Password should contain at least 1 number & 1 lower case & 1 upper case & 6 digits combination', 
                        str(messages[0]))
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_input_pw_double_check_fail(self):
        response = self.client.post("/accounts/userregister/",
                                     {'username':'dragonbrucelee@gmail.com',
                                      'password':'12345Att',
                                      'checkpassword':'ttA12345',
                                      'siterule':'YES'
                                      }
                                    )
        
        self.assertEqual(response.status_code, 200)
        
        messages = list(response.context['messages'])
        
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.ERROR])
        self.assertEqual('Passwords does not identical.', 
                        str(messages[0]))
        
        
    def test_new_user_create(self):
        response = self.client.post("/accounts/userregister/",
                                     {'username':'dragonbrucelee@gmail.com',
                                      'password':'12345Att',
                                      'checkpassword':'12345Att',
                                      'siterule':'YES'
                                      }
                                    )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        
    def tearDown(self):
        pass

'''
'''
class RegPageTest(TestCase):
    def test_url(self):
        response = self.client.post("/accounts/register/", #test URL
                                    {'flag' : ''})#test value attached in POST
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get("/accounts/register/")
        self.assertEqual(response.status_code, 200)
        
        
class LoginPageTest(TestCase):
    def test_url(self):
        #test GET
        response = self.client.get("/accounts/")#test value attached in POST
        self.assertEqual(response.status_code, 200)
        
        #test POST
        response = self.client.post("/accounts/",
                                    {'username':'nelley',
                                     'password':'123456'})#test value attached in POST
        self.assertEqual(response.status_code, 200)
        

class HomePageTest(TestCase):

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)
        
    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        
        response = home_page(request)
        
        self.assertEqual(Item.objects.count(), 1)  #1
        new_item = Item.objects.first()  #2
        self.assertEqual(new_item.text, 'A new list item')  #3
        
    
    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
    
class ListViewTest(TestCase):
    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/') #1
        print response.content
        self.assertContains(response, 'itemey 1') #2
        self.assertContains(response, 'itemey 2') #3
        
        
        
'''