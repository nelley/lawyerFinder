from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'accounts.views.login_view', name='login'),
    url(r'^register/', 'accounts.views.register_view', name='register'),
]