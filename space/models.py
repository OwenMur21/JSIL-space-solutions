from django.db import models
import datetime as dt
from django.contrib.auth.models import User

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