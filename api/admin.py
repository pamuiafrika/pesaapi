from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Plan, RequestLog, Subscription, User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'name', 'api_key','is_staff']
    search_fields = ['email', 'name','api_key']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(RequestLog)

admin.site.register(Plan)
admin.site.register(Subscription)
