from django.conf.urls import patterns, url
from inventory import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='inventory/index.html'), name='index'),
    url(r'^experiments/$', views.experiment_index, name='experiment_index'),
	url(r'^experiments/(?P<experiment_name_url>\w+)/$', views.experiment, name='experiment'), 
    url(r'^experiments/tagged/(?P<tag_url>\w+)/$', views.tag, name='tag'),
    url(r'^rooms/$', views.room_index, name='room_index'),
    url(r'^rooms/(?P<room_number>\w+)/$', views.room, name='room'),
)
