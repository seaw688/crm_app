from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from  django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birth',)}),
    )

    model = UserModel


admin.site.register(UserModel, CustomUserAdmin)