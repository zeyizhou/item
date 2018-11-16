from django.contrib import admin


from django.contrib import admin

# Register your models here.
from .models import Item
from import_export import resources
from import_export.admin import ImportExportModelAdmin




class ItemResource(resources.ModelResource):

    class Meta:
        import_id_fields = ('name',)
        skip_unchanged = True
        model = Item


class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource

admin.site.register(Item,ItemAdmin)