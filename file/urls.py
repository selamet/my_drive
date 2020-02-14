from django.contrib import admin
from django.urls import path

from file.views import model_form_upload, category_detail, add_file

urlpatterns = [
    path('form/', model_form_upload, name='model-form-upload'),
    path('categories/<slug>/', category_detail, name='category-detail'),
    path('add-file/', add_file, name='add-file'),
]
