# Generated by Django 5.0.7 on 2024-08-02 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0003_product_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.AlterField(
            model_name='tedad',
            name='name',
            field=models.IntegerField(verbose_name='تعداد'),
        ),
    ]
