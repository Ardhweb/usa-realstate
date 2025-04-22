from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
# Register your models here.
from django.db.models import ForeignKey, OneToOneField
from django.contrib.auth import get_user_model
from .models import User,RemoveRequest
from django.utils.html import format_html
admin.site.register(User)
from django import forms
from django.http import HttpResponseRedirect
from django.apps import apps
from transactions_module.models import HelcimInfo

class RemoveRequestAdmin(admin.ModelAdmin):
    change_form_template = "admin/accounts/RemoveRequest/change_form.html"
    list_display = ('__str__',"request_at",'user', 'related_model_info')
    #readonly_fields = ('related_model_info',)
    readonly_fields = ('related_info',)
    actions = ['delete_selected_related_records']


    def __str__(self, obj):
        return obj.__str__()

    @admin.display(description='Related Info')
    def related_model_info(self, obj):
        try:
            related = HelcimInfo.objects.get(user=obj.user)
            #return related.customercode
            if related:
                # Return multiple fields from the related model
                return format_html(
                '<h4>Request User Information</h4>'
                '<table style="border-collapse: collapse; width: 100%;">'
                '<tr><th style="border: 1px solid #ddd; padding: 8px;">Customer Code</th>'
                '<td style="border: 1px solid #ddd; padding: 8px;">{}</td></tr>'
                '<tr><th style="border: 1px solid #ddd; padding: 8px;">Helcim Customer Id</th>'
                '<td style="border: 1px solid #ddd; padding: 8px;">{}</td></tr>'
                '<tr><th style="border: 1px solid #ddd; padding: 8px;">Email</th>'
                '<td style="border: 1px solid #ddd; padding: 8px;">{}</td></tr>'
                '<tr><th style="border: 1px solid #ddd; padding: 8px;">First Name</th>'
                '<td style="border: 1px solid #ddd; padding: 8px;">{}</td></tr>'
                '<tr><th style="border: 1px solid #ddd; padding: 8px;">Last Name</th>'
                '<td style="border: 1px solid #ddd; padding: 8px;">{}</td></tr>'
                '<tr><th style="border: 1px solid #ddd; padding: 8px;">Membership</th>'
                '<td style="border: 1px solid #ddd; padding: 8px;">{}</td></tr>'
                '</table>',
                related.customercode, related.customerId, related.user.email, related.user.first_name, related.user.last_name ,related.user.member_type
            )
            return "No related info"
        except HelcimInfo.DoesNotExist:
            return "No related info"

    def related_info(self, obj):
        return self.related_model_info(obj)

    def get_urls(self):
        # Get the default URLs first
        urls = super().get_urls()

        # Add custom URL for the delete action
        custom_urls = [
            path(
                '<path:object_id>/delete-user-related/',
                self.admin_site.admin_view(self.delete_related_records_view),
                name='accounts_removerequest_delete_user_related',  # This name must match
            ),
        ]
        
        return custom_urls + urls

    def delete_related_records_view(self, request, object_id):
        removereq = self.get_object(request, object_id)

        if not removereq:
            self.message_user(request, "RemoveRequest not found.", level=messages.ERROR)
            return HttpResponseRedirect("../")

        user = removereq.user  # Assuming the user field is available on RemoveRequest model
        
        # Get all related models
        user_model = get_user_model()
        related_models = []

        for model in apps.get_models():
            if model in [user_model, removereq.__class__]:
                continue  # Skip the user or RemoveRequest model itself

            for field in model._meta.get_fields():
                if isinstance(field, (ForeignKey, OneToOneField)) and field.related_model == user_model:
                    related_models.append((model, field.name))
                    break

        # Delete related objects
        for model, user_field in related_models:
            filter_kwargs = {user_field: user}
            deleted = model.objects.filter(**filter_kwargs).delete()
            print(f"Deleted from {model.__name__}: {deleted}")

        # Now delete the RemoveRequest and User
        removereq.delete()
        user.delete()

        self.message_user(request, f"✅ Deleted all related records, request, and user.", level=messages.SUCCESS)
        return HttpResponseRedirect("/admin/")  # Redirect to the admin homepage

admin.site.register(RemoveRequest, RemoveRequestAdmin)
