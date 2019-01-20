from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView
import os
# from django.contrib import admin
# admin.autodiscover()

app_name='psdev'

urlpatterns = [
    url(r'', include('django.contrib.auth.urls')),

    # url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^learn/', include('learn.urls', namespace='learn')),
    # url(r'^admin/', include(admin.site.urls)),
] + static("/media/", document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static('/.well-known', document_root=os.path.dirname(settings.BASE_DIR) + '/.well-known')

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls))
    ]
