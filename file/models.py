import os
from uuid import uuid4

from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from unidecode import unidecode


class Document(models.Model):
    title = models.CharField(max_length=55, blank=True, null=False)
    description = models.CharField(max_length=255, blank=True, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)  # new
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Yazar", blank=True, null=True)



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
        return self.title


class File(models.Model):
    document = models.ForeignKey(Document, null=True, on_delete=models.CASCADE, related_name='file')
    file = models.FileField(upload_to='documents/', verbose_name='document')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return "{}".format(self.document)

    def get_file(self):
        if self.file:
            return self.file.url


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(null=True, blank=True)  # new

    def get_unique_slug(self):
        sayi = 0
        slug = slugify(unidecode(self.name))
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


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
