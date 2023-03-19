from django.contrib import admin
from dataApi.models import itemData
from import_export.admin import ImportExportModelAdmin

# Registering model(data table)
@admin.register(itemData)
class ViewAdmin(ImportExportModelAdmin):
    pass
