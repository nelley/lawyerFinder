from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'accounts.views.repw_view', name='repw'),
    url(r'^userlogin', 'accounts.views.user_login_view', name='user_login'),
    url(r'^userregister', 'accounts.views.user_register_view', name='user_register'),
    url(r'^register/', 'accounts.views.register_lawyer_view', name='register'),
    url(r'^lawyerlogin/', 'accounts.views.lawyer_login_view', name='lawyer_login'),
]