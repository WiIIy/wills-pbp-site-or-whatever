import datetime
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Products
from main.forms import ProductForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
import requests
from django.utils.html import strip_tags
import json
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.

@csrf_exempt
def create_news_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = strip_tags(data.get("name", ""))  # Strip HTML tags
        description = strip_tags(data.get("description", ""))  # Strip HTML tags
        price = strip_tags(data.get("price", ""))  # Strip HTML tags
        category = data.get("category", "")
        thumbnail = data.get("thumbnail", "")
        is_featured = data.get("is_featured", False)
        user = request.user
        
        new_product = Products(
            name=name, 
            price=price,
            category=category,
            description=description,
            thumbnail=thumbnail,
            is_featured=is_featured,
        )
        new_product.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)


@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get('filter', 'all')  # default to 'all'

    if filter_type == "my":
        products_list = Products.objects.filter(seller=request.user)
    else:
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
        product_entry = form.save(commit=False)
        product_entry.seller = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "form.html", context)

def edit_product(request, id):
    product = get_object_or_404(Products, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

@login_required(login_url='/login')
def show_products(request, id):
    products = get_object_or_404(Products, pk=id)
    products.on_click()

    context = {
        'products': products
    }

    return render(request, "products.html", context)

def delete_product(request, id):
    product = get_object_or_404(Products, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def show_xml(request):
     products_list = Products.objects.all()
     xml_data = serializers.serialize("xml", products_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    products_list = Products.objects.all()
    data = [
        {
            'id': str(products.id),
            'name': products.name,
            'price': products.price,
            'category': products.category,
            'thumbnail': products.thumbnail,
            'description': products.description,
            'is_featured': products.is_featured,
            'seller': products.seller.username if products.seller else "N/A",
        }
        for products in products_list
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, products_id):
   try:
       products_item = Products.objects.filter(pk=products_id)
       xml_data = serializers.serialize("xml", products_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except products.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, products_id):
    try:
        products = Products.objects.select_related('seller').get(pk=products_id)
        data = {
            'id': str(products.id),
            'name': products.name,
            'price': products.price,
            'category': products.category,
            'thumbnail': products.thumbnail,
            'description': products.description,
            'is_featured': products.is_featured,
            'seller': str(products.seller),
        }
        return JsonResponse(data)
    except Products.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

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

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
    seller = request.user

    new_product = Products(
        name=name, 
        price=price,
        description=description,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        seller=seller
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def edit_product_ajax(request, id):
    try:
        prod = Products.objects.get(pk=id)
    except Products.DoesNotExist:
        return HttpResponse(b"NOT FOUND", status=404)

    prod.name = request.POST.get("edit-name")
    prod.price = request.POST.get("edit-price")
    prod.description = request.POST.get("edit-description")
    prod.category = request.POST.get("edit-category")
    prod.thumbnail = request.POST.get("edit-thumbnail")
    prod.is_featured = request.POST.get("edit-is_featured") == 'on'
    


    prod.save()

    return HttpResponse(b"UPDATED", status=200)