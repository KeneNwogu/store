import json

from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm, FileField, Field
# from djongo.models.fields import JSONField
from django_json_widget.widgets import JSONEditorWidget
from djongo.models import JSONField

from .models import Product


class JSONParsedField(Field):
    def to_python(self, value):
        if not value:
            return []
        return json.loads(value)

    def validate(self, value):
        super().validate(value)
        try:
            json.loads(value)
        except:
            return ValidationError('Invalid JSON String')


class ProductForm(ModelForm):
    images = FileField(widget=forms.FileInput(attrs={'multiple': True}))

    class Meta:
        model = Product
        exclude = ('retailer',)


# Register your models here.
@admin.register(Product)
class ProductModel(admin.ModelAdmin):
    form = ProductForm
