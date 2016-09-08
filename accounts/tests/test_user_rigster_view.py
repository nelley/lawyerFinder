from django.core.urlresolvers import resolve
from django.test import TestCase
from lawyerFinder.views import home_page
from accounts.views import *
from django.http import HttpRequest
from django.template.loader import render_to_string
from lawyerFinder.models import *
from accounts.models import *
from django.utils.translation import ugettext_lazy as _
from lawyerFinder.settings import *
from django.test import TestCase, override_settings
from django.test import Client


# Create your tests here.
class user_register_test(TestCase):
    #fixtures = [FIXTURE_DIRS + 'initial_data.json']
        
    def setUp(self):
        pass
    
    def test_resolves_to_user_register_view(self):
        found = resolve('/accounts/userregister/')
        self.assertEqual(found.func, user_register_view)
        
    def test_register_page_returns_correct_html(self):
        request = HttpRequest()
        response = user_register_view(request)
        agreement_regform = User_reg_form()
        expected_html = render_to_string('accounts/register_user.html',
                                         {'user_reg_form':agreement_regform,
                                          'service_url':SITE_URL+'site_service_rule/'})
        
        self.assertEqual(response.content.decode(), expected_html)
        
        
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_input_pw_with_no_alphabet(self):
        response = self.client.post("/accounts/userregister/", #test URL
                                     {'username':'dragonbrucelee@gmail.com',
                                      'password':'123456',
                                      'checkpassword':'123456',
                                      'siterule':'YES'
                                      }
                                    )
        
        self.assertEqual(response.status_code, 200)
        
        messages = list(response.context['messages'])
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.ERROR])
        self.assertEqual('Password should contain at least 1 number & 1 lower case & 1 upper case & 6 digits combination', 
                        str(messages[0]))
    
    
    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
    def test_input_pw_length_less_than_six(self):
        response = self.client.post("/accounts/userregister/",
                                     {'username':'dragonbrucelee@gmail.com',
                                      'password':'1456',
                                      'checkpassword':'1456',
                                      'siterule':'YES'
                                      }
                                    )
        
        self.assertEqual(response.status_code, 200)
        
        messages = list(response.context['messages'])
        
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[message_constants.ERROR])
        self.assertEqual('Password should be longer than 6 digits', 
                        str(messages[0]))
    
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