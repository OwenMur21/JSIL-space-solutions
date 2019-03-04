from __future__ import unicode_literals
from django.db import models
from django.conf import settings
import datetime as dt
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from multiprocessing import Process
from django.urls import reverse

User = get_user_model()

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def save_category(self):
        self.save()

    def delete_category(self):
        self.delete()

class Product(models.Model):
    '''
    class that contains product properties,methods and functions
    '''
    post = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=40)
    posted_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    category = models.ForeignKey(Category)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    supply_date = models.DateTimeField()

    def __str__(self):
      return self.name

    def save_product(self):
        self.save

    def delete_product(self):
        self.delete

    class Meta:
        ordering = ['posted_on']

    @classmethod
    def get_all_products(cls):
        products = cls.objects.order_by()
        return products

    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)

    def get_product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_product, set_product)

    @classmethod
    def get_product_by_id(cls, id):
        product = Product.objects.filter(user_id=id).all()
        return product

    @classmethod
    def search_products(cls,name):
        product =  cls.objects.filter(category__name__icontains=name)
        return product

    @classmethod
    def filter_by_category(cls, category):
        products = cls.objects.filter(category__name__icontains=category)
        return products

    @property
    def count_likes(self):
        likes = self.likes.count()
        return likes


    @property
    def count_comments(self):
        comments = self.comments.count()
        return comments

class Profile(models.Model):
    """
    Gives users a profile
    """
    user =models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products =models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.user.username

def post_save_profile_create (sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)

class Comment(models.Model):
        """
        Class that contains comment details
        """
        comment = models.TextField()
        posted_on = models.DateTimeField(auto_now=True)
        product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
        user = models.ForeignKey(User, on_delete=models.CASCADE,null="True")

        def __str__(self):
                return self.comment

        class Meta:
                ordering = ['posted_on']
         
        def save_comment(self):
                self.save()

        def del_comment(self):
                self.delete()

        @classmethod
        def get_comments_by_product_id(cls, product):
                comments = Comment.objects.get(product_id=product)
                return comments


class Likes(models.Model):
    who_liked=models.ForeignKey(User,on_delete=models.CASCADE, related_name='likes')
    liked_product =models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')

    def save_like(self):
        self.save() 

    def __str__(self):
      return self.who_liked


class Kart(models.Model):
    product = models.ManyToManyField(Product, related_name='px')

    def __str__(self):
        return f'{self.pk} cart'


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='order')
    cart = models.ForeignKey(Kart, related_name="kx",
                             on_delete=models.DO_NOTHING)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk} Order'

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    current_qty = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name}s in stock"

# class ThreadManager(models.Manager):
#     def by_user(self, user):
#         qlookup = Q(first=user) | Q(second=user)
#         qlookup2 = Q(first=user) & Q(second=user)
#         qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
#         return qs

#     def get_or_new(self, user, other_username): # get_or_create
#         username = user.username
#         if username == other_username:
#             return None
#         qlookup1 = Q(first__username=username) & Q(second__username=other_username)
#         qlookup2 = Q(first__username=other_username) & Q(second__username=username)
#         qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
#         if qs.count() == 1:
#             return qs.first(), False
#         elif qs.count() > 1:
#             return qs.order_by('timestamp').first(), False
#         else:
#             Klass = user.__class__
#             user2 = Klass.objects.get(username=other_username)
#             if user != user2:
#                 obj = self.model(
#                         first=user, 
#                         second=user2
#                     )
#                 obj.save()
#                 return obj, True
#             return None, False


# class Thread(models.Model):
#     first        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first')
#     second       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_second')
#     updated      = models.DateTimeField(auto_now=True)
#     timestamp    = models.DateTimeField(auto_now_add=True)
    
#     objects      = ThreadManager()

#     @property
#     def room_group_name(self):
#         return f'chat_{self.id}'

#     def broadcast(self, msg=None):
#         if msg is not None:
#             broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
#             return True
#         return False


# class ChatMessage(models.Model):
#     thread      = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
#     user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
#     message     = models.TextField()
#     timestamp   = models.DateTimeField(auto_now_add=True)




class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']


class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    message = models.TextField()

    def __unicode__(self):
        return self.message


