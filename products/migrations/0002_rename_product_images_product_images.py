# Generated by Django 3.2.12 on 2022-03-04 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_images',
            new_name='images',
        ),
    ]
