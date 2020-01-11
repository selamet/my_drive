from django.db import models

# Create your models here.

from mptt.models import MPTTModel, TreeForeignKey
from django.db import models


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True,null=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']




    def __str__(self):
        return self.name
