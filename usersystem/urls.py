from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^login/$',views.login_view, name='login_view'),
        url(r'^check/$',views.check     , name='check'),
        url(r'^register/$',views.register,name='register'),
        url(r'^newUser/$',views.newUser, name='newUser'),
        url(r'^logout/$',views.logout_view,name='logout_view')
        ]
