from django.db import models


class Alert(models.Model):
    host = models.CharField(
        max_length=255,
        verbose_name="Dominio malicioso detectado",
        help_text="Dominio malicioso detectado",
    )

    referrer = models.CharField(
        max_length=255,
        verbose_name="Referrer del dominio malicioso",
        help_text="Referrer del dominio malicioso",
    )

    domain = models.ForeignKey(
        "main.Domain",
        on_delete=models.CASCADE,
        verbose_name="Dominio original suplantado",
        help_text="Dominio original suplantado",
    )

    ip = models.GenericIPAddressField(
        verbose_name="IP desde la que se lanza el canario",
        help_text="IP desde la que se lanza el canario",
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de detección",
        help_text="Fecha de detección",
    )

    revisado = models.BooleanField(
        default=False,
        verbose_name="Revisado",
        help_text="Indica si el alerta ha sido revisada por un administrador",
    )

    def get_str_content(self):
        return (
            f"{'='*50}\n"
            f"Alerta: {self.host} suplantando a {self.domain.name}\n"
            f" - IP: {self.ip}\n"
            f" - Date: {self.date}\n"
            f" - Revisado: {self.revisado}\n"
        )
    
    def __str__(self):
        return f"[Alerta]: {self.host} suplantando a {self.domain.name}"
