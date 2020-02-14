from uuid import uuid4

from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify

from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from unidecode import unidecode


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(null=True)  # new

    def get_unique_slug(self):
        sayi = 0
        slug = slugify(unidecode(self.title))
        new_slug = slug
        while Document.objects.filter(slug=new_slug).exists():
            sayi += 1
            new_slug = "%s-%s" % (slug, sayi)
        slug = new_slug
        return slug

    def save(self, *args, **kwargs):
        if self.id is None:
            self.unique_id = str(uuid4())
            self.slug = self.get_unique_slug()
        else:
            document = Document.objects.get(slug=self.slug)
            if document.title != self.title:
                self.slug = self.get_unique_slug()

        super(Document, self).save(*args, **kwargs)

        return self.title

    def __str__(self):
        return self.description


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(null=True)  # new

    def get_unique_slug(self):
        sayi = 0
        slug = slugify(unidecode(self.title))
        new_slug = slug
        while Category.objects.filter(slug=new_slug).exists():
            sayi += 1
            new_slug = "%s-%s" % (slug, sayi)
        slug = new_slug
        return slug

    class MPTTMeta:
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):
        if self.id is None:
            self.unique_id = str(uuid4())
            self.slug = self.get_unique_slug()
        else:
            category = Category.objects.get(slug=self.slug)
            if category.name != self.name:
                self.slug = self.get_unique_slug()

        super(Category, self).save(*args, **kwargs)

        return self.name

    def __str__(self):
        return self.name
