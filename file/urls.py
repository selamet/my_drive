from django.contrib import admin
from django.urls import path

from file.views import model_form_upload

urlpatterns = [
    path('form/', model_form_upload, name='model-form-upload'),
]
