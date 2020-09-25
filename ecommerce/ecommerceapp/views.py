import os
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from .forms import UserLoginForm
import pandas as pd
import numpy as np
df = pd.read_csv('similar_item.csv')

def home(request):
    items = Item.objects.all().order_by('id')[107:117]
    items_all = Item.objects.all()
    if request.method == 'POST':
        item = Item.objects.get(id = request.POST.get('iditem'))
        return redirect(f'cart/{item.id}/')
    if request.user.is_authenticated:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer)
        user_items_count = 0
        for order in orders:
            user_items_count = user_items_count + order.orderitem_set.count()
    else:
        user_items_count = 0
    context = {'objects' : items, 'items_all' : items_all, 'user_items_count' : user_items_count}
    return render(request, 'home.html', context)

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user =authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            messages.info(request, 'User name or Password incorrect ')

    return render(request, 'login.html')

def userlogout(request):
    logout(request)
    return redirect('login')

def register(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'You have been subscribe succefelly')
            Customer.objects.create(
                user=user,
                name=user.username,
            )

    context = {'form' : form}

    return render(request, 'register.html', context)

@login_required(login_url='login')
def checkout(request):
    items_all = Item.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer)
        user_items_count = 0
        for order in orders:
            user_items_count = user_items_count + order.orderitem_set.count()
        
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order_total = 0
        user_items_count = 0
        order = {'order_total' : order_total, 'user_items_count' : user_items_count}
    

    context  = {'items':items, 'order':order, 'items_all' : items_all, 'user_items_count' : user_items_count}
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def updateditem(request):
    data = json.loads(request.body)
    itemid = data['itemid']
    action = data['action']
    print('itemid :', itemid)
    print('action :', action)
    if(action == 'remove'):
        customer = request.user.customer
        order = Order.objects.get(customer=customer)
        item, created = Orderitem.objects.get_or_create(order=order,id=itemid)
        print('item : ', item)
        print('customer :', customer)
        item.delete()
    elif(action == 'add'):
        customer = request.user.customer
        order = Order.objects.get(customer=customer)
        item, created = Orderitem.objects.get_or_create(order=order,id=int(itemid))
        
        item.quantity += 1
        print(item)
        item.save()
    elif(action == 'add_item'):
        customer = request.user.customer
        order = Order.objects.get(customer=customer)
        item = Item.objects.get(id = int(itemid))
        item, created = Orderitem.objects.get_or_create(order=order, item=item)
        
        item.quantity += 1
        print(item)
        item.save()

    elif(action == 'sub'):
        customer = request.user.customer
        order = Order.objects.get(customer=customer)
        item, created = Orderitem.objects.get_or_create(order=order,id=itemid)
        if(item.quantity <= 1):
            item.delete()
        else:
            item.quantity -= 1
            print(item.quantity)
            item.save()

    return JsonResponse('IT WAS ADDED', safe = False)

def cart(request, id):
    if request.user.is_authenticated:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer)
        user_items_count = 0
        for order in orders:
            user_items_count = user_items_count + order.orderitem_set.count()
    else:
        messages.info(request, 'Signup to start shopping ')
        user_items_count = 0
        order = { 'user_items_count' : user_items_count}

    item  = Item.objects.get(id=id)
    r = (df.iloc[1:11][str(id)] +1).to_list()
    items = Item.objects.filter(id__in = r)
    items_all = Item.objects.all()
    
    context = {'objects' : items, 'items_all':items_all,
                   'item' : item, 'items_all' : items_all, 'user_items_count' : user_items_count}
    return render(request, 'cart.html', context)