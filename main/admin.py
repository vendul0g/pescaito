from django.contrib import (
    admin,
    messages,
)
from django.db.models import QuerySet
from django.http import HttpRequest

from django.utils.safestring import mark_safe
from main.models import (
    Domain,
    Project,
)
from django.conf import settings


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
    # Recorremos los dominios seleccionados por la acción y sacamos el resultado
    for domain in queryset: 
        # Llamamos al analizador de dominios
        result_file_name = domain.analyse()
        file_url = request.build_absolute_uri(settings.MEDIA_URL + result_file_name)
        # TODO Manejar errores sobre los valores de url_result
        # Devolvemos la respuesta a la interfaz web
        answer = mark_safe(f"Análisis de {domain.name} completado. Consulta el resultado <a href='{file_url}'>aquí</a>.")
        messages.success(request, answer)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", "created")
    list_filter = ("created",)

    search_fields = ("name", "project__name")

    autocomplete_fields = ("project",)

    readonly_fields = ("created",)

    actions = (analyse_domains,)
