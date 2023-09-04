# Generated by Django 4.2.4 on 2023-08-16 08:58

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('LibManager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='release_data',
            new_name='Publication_date',
        ),
        migrations.AddField(
            model_name='book',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
    ]
