from typing import Any

from django.db import models

from analysis.domain_analyser import DomainAnalyser


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
        return self.name


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

    class Meta:
        verbose_name = "dominio"
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.name

    def analyse(self) -> list[Any]:
        return DomainAnalyser(self.name).analyse()
