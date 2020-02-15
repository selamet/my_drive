from django.shortcuts import render, redirect, get_object_or_404

from file.forms import DocumentForm
from file.models import Category, Document
from mptt.forms import MoveNodeForm


def home(request):
    categories = Category.objects.all()
    documents = Document.objects.all()
    context = {'categories': categories, 'documents': documents}
    return render(request, 'home.html', context=context)


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, '../static/table/file/model_form_upload.html', {
        'form': form
    })


def category_detail(request, slug):
    context = {
        'slug': slug
    }
    return render(request, 'category_detail.html', context=context)


def parent_categories(request, slug):
    parent_category = Category.objects.get(slug=slug)

    sub_categories = Category.objects.filter(parent=parent_category)
    if sub_categories:
        arr = []
        for i in sub_categories:
            arr.append(i.slug)
        documents = Document.objects.filter(category__slug__in=arr)
    else:
        documents = Document.objects.filter(category__slug=slug)

    context = {
        'documents': documents,
        'sub_categories': sub_categories,
        'parent_category': parent_category
    }
    return render(request, 'parent_categories_detail.html', context=context)


def add_file(request):
    categories = Category.objects.all()
    context = {'categories': categories
               }

    return render(request, 'add_file.html', context=context)


def document_detail(request, slug):
    context = {
        'slug': slug
    }
    return render(request, 'document_detail.html', context=context)
