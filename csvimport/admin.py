from django.contrib import admin
import reversion
from . import models

def get_list_display(model):
    return ['__unicode__'] + [f.name for f in model._meta.fields]

def get_all_fields(model):
    return [f.name for f in model._meta.fields]

def get_search_fields(model):
    return [f.name for f in model._meta.fields]

##################
# Base Admin Class
##################

class CSVImportAdmin(reversion.VersionAdmin):
    save_as = True
    list_display = get_list_display(models.CSVImport)
    list_filter = get_all_fields(models.CSVImport)
    search_fields = get_search_fields(models.CSVImport)

admin.site.register(models.CSVImport, CSVImportAdmin)