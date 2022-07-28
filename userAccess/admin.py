
from django.contrib import admin
# Register your models here.
# linking dashboard with the database part

# since using a cusotm usermodel, making sure its visible in django admins...
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # custom display order.
    list_display = ["id", "username", "email", "date_joined",
                    "last_login", "is_staff", "is_active", "password"]


admin.site.register(CustomUser, CustomUserAdmin)
