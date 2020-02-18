from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import re

from file.models import Document, Category, File


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'description')

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'class': 'form-control m-3'}
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 5, 'cols': 20,'class':'form-control m-3'})

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            msg = 'Lütfen en az minimum 5  karakter giriniz '
            raise forms.ValidationError(msg)
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 5:
            msg = 'Lütfen en az minimum 5  karakter giriniz '
            raise forms.ValidationError(msg)
        return description


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, max_length=50, label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Hatalı kullanıcı adı veya parola girdiniz.')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if re.match(r"[^@]+@[^@]+\.[^@]+", username):
            users = User.objects.filter(email__iexact=username)
            if len(username) > 0 and len(users) == 1:
                return users.first().username
        return username
