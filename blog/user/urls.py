from django.conf.urls import url

from blog import settings
from user import views


urlpatterns = [
    url(r"^register/", views.register, name='register'),
    url(r"^login/", views.login, name='login'),
    url(r'^index/', views.index),
    url(r'^user_info/(\d+)/$', views.user_info,name='user_info'),
    url(r'^sendmail/', views.sendMail)
]