# Generated by Django 3.2.12 on 2022-03-04 02:20

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=20)),
                ('currency', models.CharField(max_length=3)),
                ('price', models.IntegerField()),
                ('in_stock', models.BooleanField()),
                ('description', models.TextField(default='No details for this product')),
                ('product_images', djongo.models.fields.JSONField()),
                ('gender', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=400)),
            ],
        ),
    ]
