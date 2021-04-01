from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import CustomUserChangeForm, RegistrationForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    
    form = CustomUserChangeForm
    add_form = RegistrationForm
    model = CustomUser
    
    list_display = ('email', 'username', 'is_staff',)
    list_filter = ('is_staff', 'is_active',)
    search_fields = ('email', 'username',)
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    # In the fieldsets, the innerst data must be tuple(if it has one element, needs comma) or list.
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('username', 'avatar',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
    )
    
    # for Creating user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2',),
        }),
    )
    # without this filter horizontal values, I am not able to allocate any permissions to users..
    # So just copied from UserAdmin source code..
    filter_horizontal = ('groups', 'user_permissions',)
    
    
admin.site.register(CustomUser, CustomUserAdmin)