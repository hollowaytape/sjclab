from django.conf.urls import patterns, url
from inventory import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='inventory/index.html'), name='index'),
    url(r'^experiments/$', views.experiment_index, name='experiment_index'),
	url(r'^experiments/(?P<experiment_name_url>\w+)/$', views.experiment, name='experiment'), # New!,
)
