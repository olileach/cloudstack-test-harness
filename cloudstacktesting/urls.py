from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from testplatform import views
from testresults.views import results
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^$',direct_to_template, {'template':'index.html'}),
    (r'^testplatform/$', views.testcriteria), 
    (r'^testresults/(?P<test_id>\d+)/$', results),
)
