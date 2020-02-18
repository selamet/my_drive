from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect, Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from file.forms import DocumentForm, FileForm, LoginForm
from file.models import Category, Document, File


@login_required(login_url=reverse_lazy('user-login'))
def home(request):
    categories = Category.objects.all()
    documents = Document.objects.all()
    context = {'categories': categories, 'documents': documents}
    return render(request, 'home.html', context=context)


@login_required(login_url=reverse_lazy('user-login'))
def category_detail(request, slug):
    context = {
        'slug': slug
    }
    return render(request, 'category_detail.html', context=context)


@login_required(login_url=reverse_lazy('user-login'))
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


@login_required(login_url=reverse_lazy('user-login'))
def upload_file_step1(request, slug):
    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            category = get_object_or_404(Category, slug=slug)
            doc = form.save(commit=False)
            doc.user = request.user
            doc.category = category
            doc.save()
            slug = doc.slug
            url = reverse('basic-upload', kwargs={'slug': slug})
            return HttpResponseRedirect(url)
    return render(request, 'create-document.html', context={'form': form})


@login_required(login_url=reverse_lazy('user-login'))
def upload_file(request, slug):
    if request.user != get_object_or_404(Document, slug=slug).user:
        raise Http404("Bu gönderiye dosya ekleyemezsiniz.")
    else:
        if request.method == 'GET':
            doc = get_object_or_404(Document, slug=slug)
            context = {

                'doc': doc
            }
            return render(request, 'add_file.html', context=context)
        elif request.method == 'POST':
            form = FileForm(request.POST, request.FILES)
            doc = get_object_or_404(Document, slug=slug)
            if form.is_valid():
                file = form.save(commit=False)
                file.document = doc
                file.save()
                data = {'is_valid': True, 'name': file.document.title, 'url': file.file.url}
            else:
                data = {'is_valid': False}
            return JsonResponse(data)


@login_required(login_url=reverse_lazy('user-login'))
def document_detail(request, slug):
    doc = get_object_or_404(Document, slug=slug)
    doc_file = File.objects.filter(document=doc)
    context = {
        'doc': doc,
        'doc_file': doc_file
    }
    return render(request, 'document_detail.html', context=context)


def user_login(request):
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

    return render(request, 'login.html', context={'form': form})


@login_required(login_url=reverse_lazy('user-login'))
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user-login'))


@login_required(login_url='/user/login/')
def doc_remove(request, slug):
    doc = get_object_or_404(Document, slug=slug)
    if request.user != doc.user:
        return HttpResponseForbidden
    doc.delete()
    return redirect('home')
