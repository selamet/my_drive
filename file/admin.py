from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from file.models import Document, Category


# Register your models here.


class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_indent_field = "some_node_field"


admin.site.register(Document)
admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)