from django.db import models
from main.models import Domain

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

    # Indica si el dominio parecido es phishing
    is_phishing = models.BooleanField(
        default=False,
        verbose_name="Es Phishing?",
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
        label_width = 45 # Ancho de la etiqueta
        return (
            f"{self.__get_verbose_name('name'):{label_width}}{self.name}\n"
            f"{self.__get_verbose_name('original_domain'):{label_width}}{self.original_domain}\n"
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
