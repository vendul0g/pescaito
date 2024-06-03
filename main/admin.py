import json
import hashlib
from django.contrib import (
    admin,
    messages,
)
from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.conf import settings
from main.models import (
    Domain,
    Project,
)


class DomainInline(admin.TabularInline):
    model = Domain

    extra = 1
    show_change_link = True
    readonly_fields = ("created",)


class JSONURLField(forms.CharField):
    def to_python(self, value):
        if not value:
            return []
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON format. Please enter a valid JSON array of URLs.")

    def validate(self, value):
        super().validate(value)
        validator = URLValidator()
        for url in value:
            validator(url)


class DomainForm(forms.ModelForm):
    urls = JSONURLField(
        widget=forms.Textarea,
        required=False,
        help_text="Introduce las URLs en formato JSON, p.e., [\"https://example.com\", \"https://anotherexample.com\"]",
    )

    def clean_urls(self):
        urls = self.cleaned_data['urls']
        cleaned_urls = []
        validator = URLValidator()
        for url in urls:
            url = url.strip()
            if url:
                try:
                    validator(url)
                    cleaned_urls.append(url)
                except ValidationError:
                    raise ValidationError(f"{url} is not a valid URL")
        return cleaned_urls

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Generamos el token si no está definido
        if not instance.token:
            instance.token = hashlib.sha256(instance.name.encode()).hexdigest()
        if commit:
            instance.save()

        # Generamos los canary token
        instance.generate_canary_token()

        return instance

    class Meta:
        model = Domain
        fields = "__all__"


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
        answer = mark_safe(
            f"Análisis de {domain.name} completado. Consulta el resultado <a href='{file_url}'>aquí</a>."
        )
        messages.success(request, answer)

@admin.action(description="Generar Canary Token")
def generate_canary_token(
    modeladmin: "DomainAdmin", request: HttpRequest, queryset: "QuerySet['Domain']"
) -> None:
    for domain in queryset:
        # Generamos el token canario
        url = domain.generate_canary_token()
        file_url = request.build_absolute_uri(settings.MEDIA_URL + url)
        # Devolvemos la respuesta a la interfaz web
        answer = mark_safe(
            f"Token canario para {domain.name} generado. Consulta el fichero <a href='{file_url}'>aquí</a>."
        )
        messages.success(request, answer)

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    form = DomainForm
    list_display = ("name", "created")
    list_filter = ("created",)

    search_fields = ("name", "project__name")

    autocomplete_fields = ("project",)

    readonly_fields = ("created","token","canary_token")

    url_fields = ("canary_token",)
    
    actions = (analyse_domains,generate_canary_token)