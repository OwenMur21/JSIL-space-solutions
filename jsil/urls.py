from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('space.urls')),
    url(r'', include('user.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^logout/$', views.logout, {"next_page": '/'}),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^oauth/', include('social_django.urls',namespace="social")),
    url(r'^accounts/', include('allauth.urls')),

]
