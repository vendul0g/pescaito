# Generated by Django 5.0.4 on 2024-05-25 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_remove_domain_urls_url"),
    ]

    operations = [
        migrations.DeleteModel(
            name="URL",
        ),
    ]