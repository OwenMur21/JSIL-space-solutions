from django.conf.urls import url
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from .views import ThreadView, InboxView

app_name = 'space'
urlpatterns=[
  url('^$',views.landing,name = 'landing'),
  url(r'^comment/(?P<product_id>\d+)', views.comment, name='comment'),
  url(r'^like/(?P<product_id>\d+)', views.like, name='like'),
  url("", InboxView.as_view()),
  url(r"^(?P<username>[\w.@+-]+)", ThreadView.as_view()),


]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

