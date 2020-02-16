from django.contrib import admin
from django.urls import path

from file.views import model_form_upload, category_detail, parent_categories, document_detail, upload_file, \
    upload_file_first

urlpatterns = [
    path('form/', model_form_upload, name='model-form-upload'),
    path('categories/<slug>/', category_detail, name='category-detail'),
    path('parent-categories/<slug:slug>/', parent_categories, name='parent-categories'),
    path('document-detail/<slug:slug>/', document_detail, name='document-detail'),
    path('basic-upload/<slug:slug>', upload_file, name="basic-upload"),
    path('basic-upload/basic-upload-first/', upload_file_first, name="basic-upload-first"),
]
