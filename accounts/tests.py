from django.test import TestCase

# Create your tests here.
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