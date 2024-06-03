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
        help_text="Introduce las URLs del dominio en formato JSON. Ejemplo: [\"https://example.com\", \"https://anotherexample.com\"]",
        default=list,
        blank=True,
    )

    admin_email = models.EmailField(
        verbose_name="email de administrador",
        help_text="Introduce el email del administrador, al que llegarán las alertas.",
        blank=True,
    )

    token = models.CharField(
        verbose_name="Token",
        max_length=256,
    )

    federation_domain = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        related_name="federated_domain",
        verbose_name="Dominio con federación",
        help_text="Introduce el dominio si existe una federación con otra organización",
        blank=True,
    )

    canary_token = models.URLField(
        verbose_name="Canary Token",
        max_length=256,
        help_text="URL de los Canary Token para la protección anti-clonado del dominio",
        blank=True,
    )

    class Meta:
        verbose_name = "dominio"
        ordering = ["-created"]

    def __str__(self) -> str:
        return str(f"{self.name}")

    def analyse(self) -> str:
        # Llamamos al analizador de dominios proactivo
        # Devolvemos el nombre del fichero donde se han volcado los datos
        from proactive_analysis.proactive_analyser import PROACTIVE_ANALYSER

        return PROACTIVE_ANALYSER.proactive_analysis(self)

    def generate_canary_token(self) -> str:
        # Generamos el token canario
        from canary.token_generator import TOKEN_GENERATOR

        return TOKEN_GENERATOR.generate_canary_token(self)
