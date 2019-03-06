from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib import admin

app_name = 'space'

urlpatterns=[
  url('^$',views.home,name = 'home'),
  url(r'^comment/(?P<product_id>\d+)', views.comment, name='comment'),
  url(r'^like/(?P<product_id>\d+)', views.like, name='like'),

  url(r'category/(?P<name>[-\w]+)',views.filter_by_category,name ='category'),

  url(r'^search/', views.search_results, name='search_results'),
  url(r'^profile/$', views.my_profile, name='my_profile'),


  url(r'^add-to-cart/(?P<item_id>\d+)/$', views.add, name='add_to_cart'),

  # url(r'^item/delete/(?P<item_id>[-\w]+)/$', views.delete_from_cart, name='delete_item'),
  url(r'^shoppingcart/remove/(?P<item_id>\d+)/$',views.remove,name='remove_from_cart'),
  url(r'^home/$', views.Home, name='chat'),
  url(r'^post/$', views.Post, name='post'),
  url(r'^messages/$', views.Messages, name='messages'),


  url(r'^cart/$',views.show,name='cart'),

  # url(r'^checkout/$', views.checkout, name='checkout'),


]
def __unicode__(self):
   return self.message

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

