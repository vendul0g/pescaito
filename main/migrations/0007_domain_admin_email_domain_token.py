# Generated by Django 5.0.4 on 2024-05-31 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_alter_domain_urls"),
    ]

    operations = [
        migrations.AddField(
            model_name="domain",
            name="admin_email",
            field=models.EmailField(
                blank=True,
                help_text="Introduce el email del administrador, al que llegarán las alertas.",
                max_length=254,
                verbose_name="email de administrador",
            ),
        ),
        migrations.AddField(
            model_name="domain",
            name="token",
            field=models.CharField(blank=True, max_length=256, verbose_name="token"),
        ),
    ]
