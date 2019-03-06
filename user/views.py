from django.shortcuts import render,redirect , get_object_or_404
from .models import *
from space.models import *
from user.models import *

from carton.cart import Cart

from multiprocessing import Process

# Create your views here.

def orders(request):
    cart = Cart(request.session)

    prods = [i.product for i in cart.items]

    nk = Kart.objects.create()
    for i in prods:
        nk.product.add(i)

    ordi = Order(cart=nk)
    ordi.save()

    # cart.clear()

    return redirect(receipt)



def supplier(request):
    orders = Order.objects.all()
    return render(request, 'orders/orders.html', locals())


def selected(request, item_id=None):
    x = Order.objects.get(pk=item_id)
    selected = Product.objects.filter(px__kx=x)
    return render(request, 'orders/order_details.html', locals())


def receipt (request):
    '''
    a receipt provided to show order has been made successfully . also send the owner an sms
    '''
    cart = Cart(request.session)
    user=request.user

    products = ', '.join(i.product.name for i in cart.items)
   

    message = "Dear "+ user.username.upper() +", your order "+products+" KES:"+str( cart.total ) + \
        " ,has been processed ! Kindly , authorize cashout ."



 

    return render (request , 'orders/receipt.html' , locals())


def order_history (request):
    '''
    user will be taken to a page containig history of all order his/her fridge has made 
    '''
    orders = Order.objects.all()
    return render( request , 'orders/history.html' ,locals() )


def order_details(request, item_id=None):
    x = Order.objects.get(pk=item_id)
    selected = Product.objects.filter(px__kx=x)

    print ( [i.price for i in selected] )

    total = sum([i.price for i in selected])

    # total = ( i.price for i in selected)
    # print( total )
    
    return render(request, 'orders/see_more.html', locals())


