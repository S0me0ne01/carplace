# Generated by Django 4.1.6 on 2023-02-16 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_product_name_kz_productcategory_name_kz_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_kz',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='description_kz',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
