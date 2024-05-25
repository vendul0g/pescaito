from django.db import models


class Project(models.Model):

    name = models.CharField(
        max_length=64,
        verbose_name="nombre",
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="fecha de creación",
    )

    class Meta:
        verbose_name = "proyecto"
        ordering = ["-created"]

    def __str__(self) -> str:
        return str(self.name)


class Domain(models.Model):

    name = models.CharField(
        primary_key=True,
        max_length=256,
        verbose_name="nombre",
    )

    project = models.ForeignKey(
        Project,
        models.CASCADE,
        related_name="domains",
        verbose_name="proyecto",
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="fecha de creación",
    )

    urls = models.JSONField(
        verbose_name="URLs",
        help_text="Enter a list of URLs.",
        default=list,
        blank=True,
    )

    class Meta:
        verbose_name = "dominio"
        ordering = ["-created"]

    def __str__(self) -> str:
        return str(f"{self.name} in {self.project} - URLs: {self.urls}")

    def analyse(self) -> str:
        # Llamamos al analizador de dominios proactivo
        # Devolvemos el nombre del fichero donde se han volcado los datos
        from proactive_analysis.proactive_analyser import PROACTIVE_ANALYSER

        return PROACTIVE_ANALYSER.proactive_analysis(self)
