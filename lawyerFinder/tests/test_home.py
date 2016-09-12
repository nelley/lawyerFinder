from django.core.urlresolvers import resolve
from django.test import TestCase
from lawyerFinder.views import *
from django.http import HttpRequest
from django.template.loader import render_to_string
from lawyerFinder.models import *
from accounts.models import *
from django.utils.translation import ugettext_lazy as _
from lawyerFinder.settings import *
from django.test import TestCase, override_settings
from django.test import Client
from common.utilities import *
from common.testUtil import *
from datetime import datetime, timedelta


# Create your tests here.
class lawyer_home_test(TestCase):
    
    def setUp(self):
        pass
    
    def test_resolves_to_home_view(self):
        found = resolve('/' )
        self.assertEqual(found.func, home)
    
    def test_home_view_returns_correct_html(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
        lawyer_searchform = Lawyer_SearchForm()
        litigation_form = LitigationTypeForm()
        barassociation_form = BarassociationForm()
        
        
        expected_html = render_to_string('base/index.html',
                                         {'lawyer_searchform':lawyer_searchform,
                                          'litigation_form':litigation_form,
                                          'barassociation_form':barassociation_form,},
                                         request=response.wsgi_request
                                         )
        
        self.assertEqual(response.content.decode(), expected_html)
        
        
    def test_home_view_search_lawyer_with_no_data(self):
        category=['IP', 'EC']
        area=['TAINAN', 'TAIPEI']
        gender=['M']
        
        response = self.client.post("/",
                                     {'category':category,
                                      'area':area,
                                      'gender':gender,
                                      }
                                    )
        
        self.assertEqual(response.status_code, 200)
        
        lawyers, areas, field = lawyerSearch(area, category, gender)
        
        expected_html = render_to_string('lawyerFinder/_search_results.html',
                                         {'queryed_lawyers':lawyers,
                                          'areas':areas,
                                          'field':field,},
                                         request=response.wsgi_request
                                         )
        
        self.assertEqual(response.content.decode(), expected_html)
        
    def test_home_view_search_lawyer_with_data(self):
        #insert lawyer data into DB
        userGenerator()
        
        category=['IP', 'EC']
        area=['TAINAN', 'TAIPEI']
        gender=['M']
        
        response = self.client.post("/",
                                     {'category':category,
                                      'area':area,
                                      'gender':gender,
                                      }
                                    )
        
        self.assertEqual(response.status_code, 200)
        
        lawyers, areas, field = lawyerSearch(area, category, gender)
        
        expected_html = render_to_string('lawyerFinder/_search_results.html',
                                         {'queryed_lawyers':lawyers,
                                          'areas':areas,
                                          'field':field,},
                                         request=response.wsgi_request
                                         )
        
        self.assertEqual(response.content.decode(), expected_html)
        