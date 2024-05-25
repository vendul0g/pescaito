# Generated by Django 5.0.4 on 2024-05-25 15:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SimilarDomain",
            fields=[
                (
                    "name",
                    models.CharField(
                        max_length=256,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Nombre de dominio parecido",
                    ),
                ),
                (
                    "found_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Fecha de aparicion"
                    ),
                ),
                (
                    "creation_date",
                    models.DateTimeField(verbose_name="Fecha de creacion del dominio"),
                ),
                (
                    "updated_date",
                    models.DateTimeField(
                        verbose_name="Fecha de ultima actualizacion del dominio"
                    ),
                ),
                (
                    "expiration_date",
                    models.DateTimeField(
                        verbose_name="Fecha de expiracion del dominio"
                    ),
                ),
                (
                    "tld_country",
                    models.CharField(
                        max_length=32, verbose_name="Pais asociado al TLD"
                    ),
                ),
                (
                    "ip_countries",
                    models.JSONField(
                        verbose_name="Paises asociados a las IPs del dominio"
                    ),
                ),
                (
                    "is_certificate_tls",
                    models.BooleanField(
                        default=False, verbose_name="Tiene certificado TLS?"
                    ),
                ),
                (
                    "tls_certificate_ca",
                    models.CharField(
                        max_length=256, verbose_name="CA del certificado TLS"
                    ),
                ),
                (
                    "tls_certificate_creation_date",
                    models.DateTimeField(
                        verbose_name="Fecha de creacion del certificado TLS"
                    ),
                ),
                (
                    "tls_certificate_oldest_date",
                    models.DateTimeField(
                        verbose_name="Fecha del certificado TLS mas antiguo"
                    ),
                ),
                (
                    "final_url",
                    models.URLField(verbose_name="URL final de las redirecciones HTTP"),
                ),
                (
                    "is_redirect_same_domain",
                    models.BooleanField(
                        default=False, verbose_name="Redirecciona al mismo dominio?"
                    ),
                ),
                (
                    "has_redirect_special_chars",
                    models.BooleanField(
                        default=False, verbose_name="Contiene caracteres especiales?"
                    ),
                ),
                (
                    "internal_links",
                    models.IntegerField(
                        default=0, verbose_name="Numero de enlaces internos"
                    ),
                ),
                (
                    "external_links",
                    models.IntegerField(
                        default=0, verbose_name="Numero de enlaces externos"
                    ),
                ),
                (
                    "is_original_domain",
                    models.BooleanField(
                        default=False, verbose_name="Referencias al dominio original?"
                    ),
                ),
                (
                    "is_login_form",
                    models.BooleanField(
                        default=False, verbose_name="Formulario de login?"
                    ),
                ),
                ("bad_links", models.JSONField(verbose_name="Enlaces enganosos")),
                (
                    "visual_similarity",
                    models.JSONField(verbose_name="Similitud visual"),
                ),
                (
                    "paas_tools",
                    models.IntegerField(
                        default=0, verbose_name="Hallazgos de herramientas PaaS"
                    ),
                ),
                (
                    "is_phishing",
                    models.BooleanField(default=False, verbose_name="Es Phishing?"),
                ),
                (
                    "last_analysis_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Ultima fecha de analisis"
                    ),
                ),
                (
                    "next_analysis_date",
                    models.DateTimeField(verbose_name="Proxima fecha de analisis"),
                ),
                (
                    "original_domain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resultados",
                        to="main.domain",
                        verbose_name="Dominio original",
                    ),
                ),
            ],
            options={
                "verbose_name": "Dominio parecido",
                "ordering": ["-found_date"],
            },
        ),
    ]
