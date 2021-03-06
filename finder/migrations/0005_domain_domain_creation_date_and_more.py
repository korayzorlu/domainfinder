# Generated by Django 4.0.4 on 2022-04-13 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0004_alter_domain_name_alter_subdomain_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='domain_creation_date',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='domain',
            name='domain_expiration_date',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='domain',
            name='domain_name_servers',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='domain',
            name='domain_registrant_name',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]
