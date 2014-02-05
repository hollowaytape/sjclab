from django.conf.urls import patterns, url
from inventory import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='inventory/index.html'), name='index'),
    url(r'^experiments/$', views.experiment_index, name='experiment_index'),
    url(r'^experiments/add/$', views.experiment_edit, {}, 'experiment_edit'),
    url(r'^experiments/edit/(?P<id>\d+)/$', views.experiment_edit, {}, 'experiment_edit'),
	url(r'^experiments/(?P<experiment_name_url>\w+)/$', views.experiment, name='experiment'), 
    url(r'^experiments/tagged/(?P<tag_name>\w+)/$', views.tag, name='tag'),
    url(r'^rooms/$', views.room_index, name='room_index'),
    url(r'^rooms/all/$', views.rooms_all, name='rooms_all'),
    url(r'^rooms/(?P<room_number>\d+)/$', views.room, name='room'),
    url(r'^rooms/edit/(?P<number>\d+)/$', views.room_edit, {}, 'room_edit'),
)
