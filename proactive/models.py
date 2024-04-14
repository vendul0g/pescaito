from django.db import models
from main.models import Domain

# Create your models here.

# Definición de la clase DomainEntryResult
# Representa el resultado del análisis de un dominio

class SimilarDomain(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=256,
        verbose_name="nombre de dominio parecido",
    )

    fecha_encontrado = models.DateTimeField(
        auto_now_add=True,
        verbose_name="fecha de aparición",
    )

    dominio = models.ForeignKey(
        Domain,
        models.CASCADE,
        related_name="resultados",
        verbose_name="dominio original",
    )

    is_phishing = models.BooleanField(
        default=False,
        verbose_name="is_phishing",
    )

    class Meta:
        verbose_name = "resultado de entrada - Dominio parecido"
        ordering = ["-fecha_encontrado"]

    def __str__(self): # TODO actualizar con los demás atributos
        return f"Domain: {self.name}"

    def __eq__(self, other):
        if isinstance(other, SimilarDomain):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)