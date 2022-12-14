from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Usuario
from django.contrib.auth.admin import UserAdmin

filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Usuario)
admin.site.register(Permission)
admin.site.register(ContentType)