from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^inventory/', include('inventory.urls')),
	url(r'^admin/', include(admin.site.urls)),
    url('^registration/', include('registration.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='https://sjclab-assets.s3.amazonaws.com/img/favicon.ico'), name='favicon'),
)

urlpatterns += staticfiles_urlpatterns()

"""if settings.DEBUG:
    urlpatterns += patterns(
	        'django.views.static',
			(r'media/(?P<path>.*)',
			'serve',
			{'document_root': settings.MEDIA_ROOT}), )"""