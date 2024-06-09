from django.contrib import admin
from .models import Alert


# Register your models here.
@admin.register(Alert)
class SimilarDomainAdmin(admin.ModelAdmin):
    list_display = ["host"]
    readonly_fields = (
        "host",
        "referrer",
        "domain",
        "ip",
        "date",
        "revisado",
    )
