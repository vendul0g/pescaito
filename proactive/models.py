from django.db import models
from main.models import Domain

# Create your models here.

# Definición de la clase DomainEntryResult
# Representa el resultado del análisis de un dominio

class SimilarDomain(models.Model):
    '''
    Atributos
    ===============================================
    '''
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
    creation_date = models.DateTimeField(
        verbose_name="Fecha de creacion del dominio"
    )

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

    # Indica si el dominio parecido es phishing
    is_phishing = models.BooleanField(
        default=False,
        verbose_name="Es Phishing?",
    )

    '''
    Métodos
    ===============================================
    '''
    class Meta:
        verbose_name = "Dominio parecido"
        ordering = ["-found_date"]

    def __get_verbose_name(self, field):
        return self._meta.get_field(field).verbose_name

    def __str__(self): # TODO actualizar con los demás atributos
        return (
                f"{self.__get_verbose_name('name')}: {self.name}\n"
                f"{self.__get_verbose_name('original_domain')}: {self.original_domain}\n"
                f"{self.__get_verbose_name('found_date')}: {self.found_date}\n"
                f"{self.__get_verbose_name('creation_date')}: {self.creation_date}\n"
                f"{self.__get_verbose_name('updated_date')}: {self.updated_date}\n"
                f"{self.__get_verbose_name('expiration_date')}: {self.expiration_date}\n"
                f"{self.__get_verbose_name('tld_country')}: {self.tld_country}\n"
                f"{self.__get_verbose_name('ip_countries')}: {self.ip_countries if self.ip_countries else 'No se encuentra país'}\n"
                f"{self.__get_verbose_name('is_phishing')}: {self.is_phishing}\n"
        )

    def __eq__(self, other):
        if isinstance(other, SimilarDomain):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)