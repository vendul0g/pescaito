from django.db import models
from main.models import Domain
import json

# Create your models here.

# Definición de la clase DomainEntryResult
# Representa el resultado del análisis de un dominio


class SimilarDomain(models.Model):
    """
    Atributos
    ===============================================
    """

    # Nombre del dominio parecido
    name = models.CharField(
        primary_key=True,
        max_length=256,
        verbose_name="Nombre de dominio parecido",
    )

    # Fecha de aparición del dominio parecido
    found_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de aparicion",
    )

    # Dominio original al que pertenece el dominio parecido
    original_domain = models.ForeignKey(
        Domain,
        models.CASCADE,
        related_name="resultados",
        verbose_name="Dominio original",
    )

    # Fecha de creación del dominio
    creation_date = models.DateTimeField(verbose_name="Fecha de creacion del dominio")

    # Fecha de ultima actualización del dominio
    updated_date = models.DateTimeField(
        verbose_name="Fecha de ultima actualizacion del dominio"
    )

    # Fecha de expiración del dominio
    expiration_date = models.DateTimeField(
        verbose_name="Fecha de expiracion del dominio"
    )

    # País asociado al TLD
    tld_country = models.CharField(
        max_length=32,
        verbose_name="Pais asociado al TLD",
    )

    # Países asociados a las IPs del dominio
    ip_countries = models.JSONField(
        verbose_name="Paises asociados a las IPs del dominio",
    )

    # Indica si el dominio tiene certificado TLS
    is_certificate_tls = models.BooleanField(
        default=False,
        verbose_name="Tiene certificado TLS?",
    )

    # Autoridad de certificación del certificado TLS
    tls_certificate_ca = models.CharField(
        max_length=256,
        verbose_name="CA del certificado TLS",
    )

    # Fecha de creación del certificado TLS
    tls_certificate_creation_date = models.DateTimeField(
        verbose_name="Fecha de creacion del certificado TLS",
    )

    # Fecha del certificado TLS más antiguo
    tls_certificate_oldest_date = models.DateTimeField(
        verbose_name="Fecha del certificado TLS mas antiguo",
    )

    # Indica la URL final de las redirecciones HTTP
    final_url = models.URLField(
        verbose_name="URL final de las redirecciones HTTP",
    )

    # Indica si la URL final de las redirecciones HTTP es el mismo dominio
    is_redirect_same_domain = models.BooleanField(
        default=False,
        verbose_name="Redirecciona al mismo dominio?",
    )

    # Indica si la URL final de redirects tiene caracteres especiales
    has_redirect_special_chars = models.BooleanField(
        default=False,
        verbose_name="Contiene caracteres especiales?",
    )

    # Indica el número de recursos a los que apunta de manera interna la página
    internal_links = models.IntegerField(
        default=0,
        verbose_name="Numero de enlaces internos",
    )

    # Indica el número de recursos a los que apunta de manera externa la página
    external_links = models.IntegerField(
        default=0,
        verbose_name="Numero de enlaces externos",
    )

    # Indica si existen referencias al dominio original
    is_original_domain = models.BooleanField(
        default=False,
        verbose_name="Referencias al dominio original?",
    )

    # Indica si en la página existe un formulario de login
    is_login_form = models.BooleanField(
        default=False,
        verbose_name="Formulario de login?",
    )

    # Indica si existen enlaces sospechosos en la página (lista de str)
    bad_links = models.JSONField(
        default=list,
        verbose_name="Enlaces enganosos",
    )

    # Indica los RMS resultantes del análisis visual (lista de floats)
    visual_similarity = models.JSONField(
        verbose_name="Similitud visual",
    )

    # Indica el número de hallazgos encontrados sobre herramientas PaaS
    paas_tools = models.IntegerField(
        default=0,
        verbose_name="Hallazgos de herramientas PaaS",
    )

    # Indica si el dominio parecido es phishing
    is_phishing = models.BooleanField(
        default=False,
        verbose_name="Es Phishing?",
    )

    # Indica el peso total de los parámetros
    total_weight = models.FloatField(
        default=0.0,
        verbose_name="Peso total",
    )

    # Indica la última fecha de análisis
    last_analysis_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Ultima fecha de analisis",
    )

    # Indica la próxima fecha de análisis
    next_analysis_date = models.DateTimeField(
        verbose_name="Proxima fecha de analisis",
    )

    """
    Métodos
    ===============================================
    """

    class Meta:
        verbose_name = "Dominio parecido"
        ordering = ["-found_date"]

    def __get_verbose_name(self, field):
        return self._meta.get_field(field).verbose_name

    def __str__(self):
        label_width = 45  # Ancho de la etiqueta
        return (
            f"{self.__get_verbose_name('name'):{label_width}}{self.name}\n"
            f"{self.__get_verbose_name('original_domain'):{label_width}}{self.original_domain.name}\n"
            f"{'':label_width}Proyecto: {self.original_domain.project.name}\n"
            f"{'':label_width}URLs: {self.original_domain.urls}\n\n"
            f"{self.__get_verbose_name('found_date'):{label_width}}{self.found_date}\n"
            f"{self.__get_verbose_name('creation_date'):{label_width}}{self.creation_date}\n"
            f"{self.__get_verbose_name('updated_date'):{label_width}}{self.updated_date}\n"
            f"{self.__get_verbose_name('expiration_date'):{label_width}}{self.expiration_date}\n"
            f"{self.__get_verbose_name('tld_country'):{label_width}}{self.tld_country}\n"
            f"{self.__get_verbose_name('ip_countries'):{label_width}}{self.ip_countries if self.ip_countries else 'No country found'}\n"
            f"{self.__get_verbose_name('is_certificate_tls'):{label_width}}{self.is_certificate_tls}\n"
            f"{self.__get_verbose_name('tls_certificate_ca'):{label_width}}{self.tls_certificate_ca}\n"
            f"{self.__get_verbose_name('tls_certificate_creation_date'):{label_width}}{self.tls_certificate_creation_date}\n"
            f"{self.__get_verbose_name('tls_certificate_oldest_date'):{label_width}}{self.tls_certificate_oldest_date}\n"
            f"{self.__get_verbose_name('final_url'):{label_width}}{self.final_url}\n"
            f"{self.__get_verbose_name('is_redirect_same_domain'):{label_width}}{self.is_redirect_same_domain}\n"
            f"{self.__get_verbose_name('has_redirect_special_chars'):{label_width}}{self.has_redirect_special_chars}\n"
            f"{self.__get_verbose_name('internal_links'):{label_width}}{self.internal_links}\n"
            f"{self.__get_verbose_name('external_links'):{label_width}}{self.external_links}\n"
            f"{self.__get_verbose_name('is_original_domain'):{label_width}}{self.is_original_domain}\n"
            f"{self.__get_verbose_name('is_login_form'):{label_width}}{self.is_login_form}\n"
            f"{self.__get_verbose_name('bad_links'):{label_width}}{self.bad_links if self.bad_links else 'No bad links found'}\n"
            f"{self.__get_verbose_name('visual_similarity'):{label_width}}{json.dumps(self.visual_similarity if self.visual_similarity else 'No visual similarity found', indent=4)}\n"
            f"{self.__get_verbose_name('paas_tools'):{label_width}}{self.paas_tools}\n\n"
            # f"{self.__get_verbose_name('last_analysis_date'):{label_width}}{self.last_analysis_date}\n"
            # f"{self.__get_verbose_name('next_analysis_date'):{label_width}}{self.next_analysis_date}\n"
            f"\n{'~'*25} Results {'~'*25}\n"
            f"{self.__get_verbose_name('total_weight'):{label_width}}{self.total_weight}\n"
            f"{self.__get_verbose_name('is_phishing'):{label_width}}{self.is_phishing}\n"
        )

    def __eq__(self, other):
        if isinstance(other, SimilarDomain):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        # Comparar por nombre para ordenar
        if isinstance(other, SimilarDomain):
            return self.name < other.name
        return NotImplemented
