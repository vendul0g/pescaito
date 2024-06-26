# Generated by Django 5.0.4 on 2024-05-31 10:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0011_alter_domain_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="domain",
            name="federation_domain",
            field=models.ForeignKey(
                help_text="Introduce el dominio si existe una federación con otra organización",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="federated_domain",
                to="main.domain",
                verbose_name="Dominio con federación",
            ),
        ),
    ]
