import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
import json
from . utils import cookieCart, cartData, guestOrder
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.models import User
# Create your views here.

def store(request):
    data = cartData(request=request)
    cartItems = data['cartItems']
        
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):

    data = cartData(request=request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
                   

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request,'store/cart.html', context)


from django.views.decorators.csrf import csrf_exempt


def checkout(request):
    data = cartData(request=request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request,'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        order, customer = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'], 
        )

    return JsonResponse('Order was added', safe=False)


from django.http import JsonResponse

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user, created = User.objects.get_or_create(username=username)
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            return redirect('login')
        
    context = {}
    return render(request, 'store/login.html', context=context)

def logoutUser(request):
    logout(request)
    return redirect('store')
     