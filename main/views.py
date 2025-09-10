from django.shortcuts import render, redirect, get_object_or_404
from main.models import Products
from main.forms import ProductForm
from django.http import HttpResponse
from django.core import serializers

# Create your views here.
def show_main(request):
    products_list = Products.objects.all()

    context = {
        'app' : 'BeliBola',
        'npm' : '240123456',
        'name': 'Haru Urara',
        'class': 'PBP A',
        'products_list': products_list, 
    }

    return render(request, "main.html", context)

def create_products(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "form.html", context)

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
