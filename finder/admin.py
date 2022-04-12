
from django.contrib import admin

from .models import Domain, Subdomain

# Register your models here.

class SubdomainAdmin(admin.StackedInline):
    model = Subdomain
    extra = 0

@admin.register(Domain)
class Domain(admin.ModelAdmin):
    list_display = ["id", "name", "created_date"]
    list_display_links = ["name", "created_date"]
    search_fields = ["name"]
    list_filter = ["created_date"]
    inlines = [SubdomainAdmin]
    class Meta:
        model = Domain


@admin.register(Subdomain)
class SubdomainAdmin(admin.ModelAdmin):
    list_display = ["name"]
    