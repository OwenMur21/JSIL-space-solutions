from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User # May not be in use
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth import login, authenticate, get_user_model
import json
import urllib
from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings
from django.contrib import messages
from .forms import *
from .models import *
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
import requests
from .decorators import check_recaptcha
from django.http import JsonResponse




def landing(request):
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

            return redirect('landing')
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
            return redirect('landing')
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
    return redirect('landing')


@login_required(login_url='/accounts/login/')
def like(request, product_id):
    current_user = request.user
    liked_product=Product.objects.get(id=product_id)
    new_like,created= Likes.objects.get_or_create(who_liked=current_user, liked_product=liked_product)
    new_like.save()

    return redirect('landing')


@login_required(login_url='/accounts/login/')
def about(request):
    return render(request,'about_us.html')

def my_profile(request):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    context = { 'my_orders': my_orders }
    return render(request, "profile.html", context)






    

    
