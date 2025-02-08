from django.contrib import admin
from .models import GuestEmail
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    #The form to add and changes de user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    #The fields to be used in displaying the User model
    #These override the definitions on the base UserAdmin
    #That reference the specific fields on auth.User
    list_display = ['email', 'admin']
    list_filter = ['admin', 'staff', 'active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')}),
    )

    #add_fieldsets is not standard ModelAdmin attribute. UserAdmin
    #overrrides get_fieldsets to use this attribute when create a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')
        }),
    )

    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
#Remove Group Model from admin. We're not using it
admin.site.unregister(Group)

class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = GuestEmail

admin.site.register(GuestEmail, GuestEmailAdmin)