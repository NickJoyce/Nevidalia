from django.contrib import admin
from django.shortcuts import redirect
from .models import CustomAdminPage, Promocode, NotificationRecipients, Settings, EmailNotificationTemplate
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib import admin
from django.contrib.auth.models import User, Group
from .utils import csv_file_handling
from django.contrib import messages
import traceback
import time
from django.http import HttpResponseRedirect


admin.site.site_title = "Admin Panel"
admin.site.site_header = "Admin Panel"

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Settings)


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ['action_name', 'date_of_create', 'start_date', 'end_date', 'park', 'creator',
                    'tilda_external_product_id', 'code', 'status', 'date_of_use', 'ticket_limit', 'ticket_day_type',
                    'customer_name', 'customer_phone', 'customer_email', 'sending_date']
    list_filter = ['park', 'creator', 'action_name', 'tilda_external_product_id', 'status']
    search_fields = ['date_of_create', 'start_date', 'end_date', 'park', 'creator', 'action_name', 'code', 'status',
                    'date_of_use', 'tilda_external_product_id', 'customer_name', 'customer_phone', 'customer_email']

    change_list_template = "admin/promocode_change_list.html"

    extra_context = {}

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('change_external_id/', self.change_external_id),
            path('file_upload/', self.file_upload),
            path('delete_by_park/', self.delete_by_park),
            path('delete_by_tilda_external_product_id/', self.delete_by_tilda_external_product_id)
        ]
        return my_urls + urls

    def change_external_id(self, request):
        if request.method == "POST":
            old = request.POST.get("old_external_id", "")
            new = request.POST.get("new_external_id", "")
            self.model.objects.filter(tilda_external_product_id=old).update(tilda_external_product_id=new)
            messages.add_message(request, messages.SUCCESS, 'Внешний код успешно изменен')
        return HttpResponseRedirect("../")

    def file_upload(self, request):
        if request.method == "POST":
            file = request.FILES['file']

            start = time.time()
            is_ok = csv_file_handling(file, request)
            end = time.time() - start
            if is_ok:
                messages.add_message(request, messages.SUCCESS, 'Данные из файла успешно загружены в БД')
                messages.add_message(request, messages.SUCCESS,
                                     f"Время обработки: {time.strftime('%H:%M:%S', time.gmtime(end))}")
        return HttpResponseRedirect("../")


    def delete_by_park(self, request, extra_context=None):
        messages.add_message(request, messages.ERROR, 'Error')
        return HttpResponseRedirect("../")


    def delete_by_tilda_external_product_id(self, request):
        messages.add_message(request, messages.ERROR, 'Error')
        return HttpResponseRedirect("../")


@admin.register(NotificationRecipients)
class NotificationRecipientsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_active']

@admin.register(EmailNotificationTemplate)
class EmailNotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ['name']





# @admin.register(CustomAdminPage)
# class CustomAdminPageAdmin(admin.ModelAdmin):
#
#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('files-upload/', self.admin_site.admin_view(self.files_upload), name="files_upload"),
#         ]
#         return my_urls + urls
#
#
#     def files_upload(self, request):
#         if request.method == "POST":
#             file = request.FILES['file']
#
#             start = time.time()
#             is_ok = csv_file_handling(file, request)
#             print(is_ok)
#             end = time.time() - start
#             if is_ok:
#                 messages.add_message(request, messages.SUCCESS, 'Данные из файла успешно загружены в БД')
#                 messages.add_message(request, messages.SUCCESS,
#                                      f"Время обработки: {time.strftime('%H:%M:%S', time.gmtime(end))}")
#
#
#             return redirect("admin:files_upload")
#         else:
#             title = "Загрузка файла"
#             context = dict(
#                # Include common variables for rendering the admin template.
#                self.admin_site.each_context(request),
#                # Anything else you want in the context...
#                title=title
#             )
#             return TemplateResponse(request, "admin/files-upload.html", context)

