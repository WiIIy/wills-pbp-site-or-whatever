from django.forms import ModelForm
from main.models import Products
from django import forms

class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = ["name", "price", "description", "thumbnail", "category","is_featured" ]
