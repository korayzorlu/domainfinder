# Generated by Django 4.0.4 on 2022-04-13 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0005_domain_domain_creation_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='domain',
            old_name='domain_creation_date',
            new_name='creation_date',
        ),
        migrations.RenameField(
            model_name='domain',
            old_name='domain_expiration_date',
            new_name='expiration_date',
        ),
        migrations.RenameField(
            model_name='domain',
            old_name='domain_name_servers',
            new_name='name_servers',
        ),
        migrations.RenameField(
            model_name='domain',
            old_name='domain_registrant_name',
            new_name='registrant_name',
        ),
    ]