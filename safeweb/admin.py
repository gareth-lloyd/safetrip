from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from safeweb.models import UserProfile

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False


class MyUserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline, ]

admin.site.register(User, MyUserAdmin)
