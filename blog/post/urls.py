from django.conf.urls import url

from post import views


urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^publish/', views.publish, name='publish'),
    url(r'^showpost/(?P<n>\d+)/', views.showpost, name='showpost'),
    url(r'^deletepost/(?P<n>\d+)/', views.deletepost, name='deletepost'),
    url(r'^comment/(\d+)/$', views.comment, name='comment'),
    url(r'^reply/(\d+)/$', views.reply, name='reply'),
]