from django.contrib import (
    admin,
    messages,
)
from django.db.models import QuerySet
from django.http import HttpRequest

from main.models import (
    Domain,
    Project,
)


class DomainInline(admin.TabularInline):
    model = Domain

    extra = 1
    show_change_link = True
    readonly_fields = ("created",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created")
    list_filter = ("created",)

    search_fields = ("name", "domains__name")

    readonly_fields = ("created",)

    inlines = (DomainInline,)


@admin.action(description="Analizar dominios")
def analyse_domains(
    modeladmin: "DomainAdmin", request: HttpRequest, queryset: "QuerySet['Domain']"
) -> None:
    for domain in queryset:
        results = domain.analyse()
        messages.info(request, f"{domain}: {results}")


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", "created")
    list_filter = ("created",)

    search_fields = ("name", "project__name")

    autocomplete_fields = ("project",)

    readonly_fields = ("created",)

    actions = (analyse_domains,)
