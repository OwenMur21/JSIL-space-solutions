from __future__ import unicode_literals
from django.db import models
from django.conf import settings
import datetime as dt
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

User = get_user_model()

# Create your models here.



class Product(models.Model):
    '''
    class that contains product properties,methods and functions
    '''
    post = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=40)
    posted_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)

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

    @classmethod
    def get_product_by_id(cls, id):
        product = Product.objects.filter(user_id=id).all()
        return product

    @classmethod
    def search_product(cls,name):
        product =  cls.objects.filter(name__icontains=name)
        return product

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