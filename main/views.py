import datetime
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Products
from main.forms import ProductForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    products_list = Products.objects.all()

    context = {
        'app' : 'BeliBola',
        'npm' : '2406404112',
        'name': 'Sherin Urara',
        'class': 'PBP B',
        'products_list': products_list, 
        'last_login': request.COOKIES.get('last_login',"Never"),
        'username': request.COOKIES.get('username', "Never")
    }

    return render(request, "main.html", context)

@login_required(login_url='/login')
def create_products(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit = False)
        product_entry.user = request.user 
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "form.html", context)

@login_required(login_url='/login')
def show_products(request, id):
    products = get_object_or_404(Products, pk=id)
    products.on_click()

    context = {
        'products': products
    }

    return render(request, "products.html", context)


def show_xml(request):
     products_list = Products.objects.all()
     xml_data = serializers.serialize("xml", products_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    products_list = Products.objects.all()
    json_data = serializers.serialize("json", products_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, products_id):
   try:
       products_item = Products.objects.filter(pk=products_id)
       xml_data = serializers.serialize("xml", products_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except products.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, products_id):
   try:
       products_item = Products.objects.get(pk=products_id)
       json_data = serializers.serialize("json", [products_item])
       return HttpResponse(json_data, content_type="application/json")
   except products.DoesNotExist:
       return HttpResponse(status=404)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
