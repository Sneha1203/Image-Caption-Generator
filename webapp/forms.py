from django.db import models
from django.forms import fields
from .models import UploadImage
from django import forms

class UserImageForm(forms.Form):
    class Meta:
        models = UploadImage
        fields = '__all__'