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
    return render(request, 'file/model_form_upload.html', {
        'form': form
    })
