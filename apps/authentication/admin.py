from django.contrib import admin

from apps.authentication.models import User, UserRating, UserAddress


class UserRatingAdmin(admin.TabularInline):
    model = UserRating


class UserAddressAdmin(admin.TabularInline):
    model = UserAddress


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'first_name', 'last_name', 'is_superuser', 'is_staff',)
    search_fields = ('email', 'phone')
    exclude = ('groups', 'user_permissions', 'password')
    inlines = [
        UserRatingAdmin,
        UserAddressAdmin
    ]


admin.site.register(User, UserAdmin)
