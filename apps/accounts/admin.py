from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ['name', 'email', 'is_superuser', 'is_staff']
    list_filter = []
    search_fields = ['name', 'email']
    filter_horizontal = []
    fieldsets = (
        (None, {'fields': ('name', 'email', 'username', 'password')}),
        ('Permissão', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin')}),
    )
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': (
        'name',
        'username', 'email',
        'password1', 'password2',
    )}),)


admin.site.register(User, CustomUserAdmin)
