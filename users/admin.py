from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from users.models import User, Relationship

# Register your models here.
# admin.site.register(User)
admin.site.register(Relationship)


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'password1',
                    'password2',
                ),
            }
        ),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password', 'introduction', 'is_public')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
