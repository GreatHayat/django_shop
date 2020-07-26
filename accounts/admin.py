from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_filter = ("user_type",)
    list_display = ("username", "email", "last_login",
                    "date_joined", "is_active", "user_type", )


admin.site.register(User, UserAdmin)
