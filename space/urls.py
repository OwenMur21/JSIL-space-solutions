from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
  url('^$',views.homepage,name = 'homepage'),
  url(r'^comment/(?P<product_id>\d+)', views.comment, name='comment'),
  url(r'^like/(?P<product_id>\d+)', views.like, name='like'),
  url(r'category/(\d+)',views.filter_by_category,name ='category'),
  url(r'^search/', views.search_results, name='search_results'),
  url(r'^profile/$', views.my_profile, name='my_profile'),
  url(r'^order-summary/$', views.order_details, name="order_summary"),
  url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name='add_to_cart'),
  url(r'^item/delete/(?P<item_id>[-\w]+)/$', views.delete_from_cart, name='delete_item'),
  # url(r'^checkout/$', views.checkout, name='checkout'),


]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

