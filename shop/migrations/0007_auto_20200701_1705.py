# Generated by Django 3.0.7 on 2020-07-01 17:05

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200701_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='long_description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]