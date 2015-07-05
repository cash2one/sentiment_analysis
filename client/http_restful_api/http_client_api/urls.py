from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('http_client_api.views',
    # Examples:
    # url(r'^$', 'http_client_api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/(?P<port>\w+)/(?P<domain>\w+)/(?P<func>\w+)/$',"api",name="tclapi"),
)
