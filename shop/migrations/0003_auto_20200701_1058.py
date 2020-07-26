# Generated by Django 3.0.7 on 2020-07-01 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_discount_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='Please leave this field as blank it will be filled automatically based on your discount percentage', max_digits=6, null=True, verbose_name='Discount Price'),
        ),
    ]