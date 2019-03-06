from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'

urlpatterns=[
    url(r'^proceed/order/$', views.orders, name='orders'),
    url(r'^orders/supplier/$', views.supplier, name='supplier'),
    url(r'^space/orders/history$', views.order_history, name='order_history'),
    url(r'^space/orders/order_details/(\d+)$', views.order_details, name='order_details'),
    url(r'^space/receipt/$', views.receipt, name='receipt'),
    url(r'^orders/order/(?P<item_id>\d+)$', views.selected, name='selected'),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
