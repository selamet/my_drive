from django.shortcuts import render, redirect, get_object_or_404

from file.forms import DocumentForm
from file.models import Category
from mptt.forms import MoveNodeForm


def home(request):
    categories = Category.objects.all()
    context = {'categories': categories}
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


def add_file(request):
    categories = Category.objects.all()
    context = {'categories': categories
               }

    return render(request, 'add_file.html', context=context)
