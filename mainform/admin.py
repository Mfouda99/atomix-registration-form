from django.contrib import admin
from .models import Registrationform
from django.utils.html import format_html


@admin.register(Registrationform)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'phone_number', 'email', 'position', 'function', 
        'view_id_front', 'view_id_back', 'view_indemnity_form', 'view_personal_photo'
    )

    # Display links for ID Front, ID Back, Indemnity Form, and Personal Photo in the admin
    def view_id_front(self, obj):
        if obj.id_front:
            return format_html('<a href="{}" target="_blank">View ID Front</a>', obj.id_front.url)
        return "No ID Front Uploaded"

    def view_id_back(self, obj):
        if obj.id_back:
            return format_html('<a href="{}" target="_blank">View ID Back</a>', obj.id_back.url)
        return "No ID Back Uploaded"

    def view_indemnity_form(self, obj):
        if obj.indemnity_form:
            return format_html('<a href="{}" target="_blank">View Indemnity Form</a>', obj.indemnity_form.url)
        return "No Indemnity Form Uploaded"

    def view_personal_photo(self, obj):
        if obj.personal_photo:
            return format_html('<a href="{}" target="_blank">View Personal Photo</a>', obj.personal_photo.url)
        return "No Personal Photo Uploaded"

    # Define column headers in the admin list view
    view_id_front.short_description = 'ID Front'
    view_id_back.short_description = 'ID Back'
    view_indemnity_form.short_description = 'Indemnity Form'
    view_personal_photo.short_description = 'Personal Photo'

