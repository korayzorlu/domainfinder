
from django.contrib import admin

from .models import Domain, Subdomain

# Register your models here.

admin.site.register(Domain)

admin.site.register(Subdomain)
class SubdomainAdmin(admin.ModelAdmin):
    list_display = ["subdomain"]