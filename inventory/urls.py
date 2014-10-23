from django.conf.urls import patterns, url
import views
from baros import settings
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='inventory/index.html'), name='index'),
    
    url(r'^experiments/$', views.experiment_index, name='experiment_index'),
    url(r'^experiments/add/$', views.experiment_edit, name='experiment_edit'),
    url(r'^experiments/edit/(?P<id>\d+)/$', views.experiment_edit, name='experiment_edit'),
	url(r'^experiments/(?P<experiment_name_url>\w+)/$', views.experiment, name='experiment'), 
    url(r'^experiments/delete/(?P<id>\d+)/$', views.experiment_delete, name='experiment_delete'),
    
    url(r'^experiments/tagged/(?P<tag_name_url>\w+)/$', views.tag, name='tag'),
    
    url(r'^rooms/$', views.room_index, name='room_index'),
    url(r'^rooms/all/$', views.rooms_all, name='rooms_all'),
    url(r'^rooms/(?P<room_url>\w+)/$', views.room, name='room'),
    url(r'^rooms/edit/(?P<room_url>\w+)/$', views.room_edit, name='room_edit'),

    url(r'^texts/add/$', views.text_add, name='text_add'),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    #url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    
    url(r'^approval/$', views.admin_user_approval, name="user_approval"),
    url(r'^approval/(?P<id>\d+)/$', views.approve_user, name="approve_user"),
)
