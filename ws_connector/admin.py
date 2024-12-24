from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Position, Credential
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class CredentialInline(admin.StackedInline):
    model = Credential
    can_delete = False
    verbose_name_plural = "credential"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [CredentialInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Position)
