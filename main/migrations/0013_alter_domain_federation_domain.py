# Generated by Django 5.0.4 on 2024-06-03 16:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_domain_federation_domain"),
    ]

    operations = [
        migrations.AlterField(
            model_name="domain",
            name="federation_domain",
            field=models.ForeignKey(
                blank=True,
                help_text="Introduce el dominio si existe una federación con otra organización",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="federated_domain",
                to="main.domain",
                verbose_name="Dominio con federación",
            ),
        ),
    ]
