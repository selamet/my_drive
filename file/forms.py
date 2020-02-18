from django import forms

from file.models import Document, Category, File


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'description')

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control m-3'}

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
