from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User # May not be in use
from django.http  import HttpResponse,Http404,HttpResponseRedirect,HttpResponseForbidden,JsonResponse
from django.contrib.auth import login, authenticate, get_user_model
import json
from jsil import settings
import urllib
from django.contrib import messages
from .forms import SignupForm,CommentForm,ComposeForm,ImageForm
from .models import *
from django.contrib import messages
from django.conf import settings
import requests
from .decorators import check_recaptcha
from django.http import JsonResponse
from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
# from .models import Thread, ChatMessage



# django - carton 
from carton.cart import Cart

#
from django.views import generic
from multiprocessing import Process

import csv





from django.urls import reverse

@login_required(login_url='/accounts/login/')
def home(request):
    products = Product.objects.all()
    comments = Comment.objects.all()
    likes = Likes.objects.all()
    return render(request, 'home.html',locals())
    
def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
  
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                form.save()
                messages.success(request, 'Account verified successfully!')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

            return redirect('homepage')
    else:
        form = SignupForm()

    return render(request, 'registration/registration_form.html', {'form': form})

@check_recaptcha
def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('homepage')
    else:
        form = SignupForm()

    return render(request, 'registration/registration_form.html', {'form': form})

@login_required(login_url='/accounts/login/')
def comment(request, product_id):
    products = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = products
            comment.save()
    return redirect('homepage')


@login_required(login_url='/accounts/login/')
def like(request, product_id):
    current_user = request.user
    liked_product=Product.objects.get(id=product_id)
    new_like,created= Likes.objects.get_or_create(who_liked=current_user, liked_product=liked_product)
    new_like.save()

    return redirect('homepage')



def filter_by_category(request,name):
    '''
    Filters the database and displays products according to category_id
    '''
    products = Product.filter_by_category(name)
    print(name)
    print(products)

    return render(request,'category.html',{"products":products})




def my_profile(request):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    context = { 'my_orders': my_orders }
    return render(request, "profile.html", context)


def add(request,item_id):

    cart = Cart(request.session)

    product = Product.objects.get(id=item_id)
    print(product)

    cart.add(product, price=product.price)

    print(cart.items)

    return redirect('space:category',name=product.category)


def show(request):
    cart = Cart(request.session)
    products = Product.objects.all()
    total=cart.total
    # subtotal=cart.subtotal()

    return render(request, 'cart.html', locals()) 

def remove(request, item_id):
    '''
    Controller function for removing an item from the cart.
    '''
    cart = Cart(request.session)
    product = Product.objects.get(id=item_id)
    cart.remove(product)
    return render(request, 'cart.html', locals())


@login_required(login_url='/accounts/login/')
def search_results(request):
  if 'product' in request.GET and request.GET["product"]:
    name = request.GET.get("product")
    searched_products = Product.search_products(name)
    message = f"{name}"

    return render(request, 'search.html',{"message":message,"products":searched_products})

  else:
    message = "You haven't searched for anything"
    return render(request, 'search.html',{"message":message})

def Home(request):
    c = Chat.objects.all()
    return render(request, "chat.html", {'home': 'active', 'chat': c})

def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        
        c = Chat(user=request.user, message=msg)
            
        
        msg = c.user.username+": "+msg

        c = Chat(user=request.user, message=msg)

        if msg != '':            
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.user.username})
    else:
        return HttpResponse('Request must be POST.')

def Messages(request):
    c = Chat.objects.all()
    return render(request, 'messages.html', {'chat': c})
