from django.contrib import admin
from django.urls import path

from file.views import category_detail, parent_categories, document_detail, upload_file, upload_file_step1
urlpatterns = [
    path('categories/<slug>/', category_detail, name='category-detail'),
    path('parent-categories/<slug:slug>/', parent_categories, name='parent-categories'),
    path('document-detail/<slug:slug>/', document_detail, name='document-detail'),
    path('basic-upload/<slug:slug>', upload_file, name="basic-upload"),
    path('upload-file-step-1/<slug:slug>', upload_file_step1, name='upload-file-step-1')
]
