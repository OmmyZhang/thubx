from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$',views.index, name='index'),
        url(r'^betting/$',views.betting, name='betting'),
        url(r'^rank/$',views.rank,name='rank'),
        url(r'^manage/$',views.manage,name='manage')
        ]
