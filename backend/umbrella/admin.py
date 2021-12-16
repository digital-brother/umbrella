from django.contrib import admin
from .models import Lease

class LeaseAdmin(admin.ModelAdmin):
  list_display = ('id', 'file_name', 'pdf', 'txt', 'extracted', 'address', 'createdon', 'createdby','modifiedon', 'modifiedby', 'activeflag', 'contract_type', 'textract', 'analyticsdata', 'pdf_hash', 'file_size', 'modified_file_name', 'analytics2', 'doc_type')

# Register your models here.
admin.site.register(Lease, LeaseAdmin)