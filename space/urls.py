from django.conf.urls import url
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
  url('^$',views.landing,name = 'landing'),
  url(r'^comment/(?P<image_id>\d+)', views.comment, name='comment'),
  url(r'^like/(?P<image_id>\d+)', views.like, name='like'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

