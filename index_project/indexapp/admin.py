from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .models import *
import csv
from io import TextIOWrapper
from .upload_csv_data import csv_data_upload
from django.utils.encoding import smart_str


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

    writer = csv.writer(response)
    '''If we are trying to download multiple csv then headr row appear twice. 
    so for resolving this issue will count the header only once.'''
    header_row_count  = 0  

    for parent_obj in queryset:
        # for field_name in DailyPrice._meta.fields:
        #     print(field_name)

        # if header_row_count = 1. It means header exist in th file.
        if header_row_count <=0:
            child_header_row = [field_name.name for field_name in DailyPrice._meta.fields]
            child_header_row.remove('id')
            writer.writerow(child_header_row)
            header_row_count +=1

        # Write data rows for ChildModel related to ParentModel
        child_queryset = DailyPrice.objects.filter(index_id=parent_obj)
        for child_obj in child_queryset:
            child_data_row = [smart_str(getattr(child_obj, field.name).name) if field.name =='index' else smart_str(getattr(child_obj, field.name)) for field in DailyPrice._meta.fields]
            child_data_row.pop(0)
            writer.writerow(child_data_row)

    return response


export_to_csv.short_description = "Export selected items to CSV"
class CustomerAdmin(admin.ModelAdmin):
    actions = [export_to_csv]
    list_display = ('name',)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            csv_data = []
            with TextIOWrapper(csv_file.file, encoding='utf-8-sig') as file_wrapper:
                csv_reader = csv.DictReader(file_wrapper)
                # import pdb;pdb.set_trace()
                for row in csv_reader:
                    row = {key.strip(): value for key, value in row.items()}
                    csv_data.append(row)
            
            response = csv_data_upload(csv_data)

            # if data not upload sucessfully then will redirect it to error page too
            if not response:
                return HttpResponseRedirect('https://colorlib.com/wp/free-404-error-page-templates/') 
            print('load')
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


# Register your models here.
admin.site.register(Index, CustomerAdmin)
admin.site.register(DailyPrice)