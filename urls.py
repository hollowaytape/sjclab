from django.conf import settings
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from inventory.views import user_login

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
	url(r'^$', user_login),
    url(r'', include('inventory.urls')),
    #url(r'^inventory/', RedirectView.as_view(pattern_name='inventory.views.user_login')),       # To preserve legacy links
	url(r'^admin/', admin.site.urls),
    url(r'^favicon\.ico$', RedirectView.as_view(url='https://sjclab-assets.s3.amazonaws.com/img/favicon.ico'), name='favicon'),
]

urlpatterns += staticfiles_urlpatterns()

"""if settings.DEBUG:
    urlpatterns += patterns(
	        'django.views.static',
			(r'media/(?P<path>.*)',
			'serve',
			{'document_root': settings.MEDIA_ROOT}), )"""