# Generated by Django 3.0.5 on 2020-04-15 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20200415_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productentry',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
    ]
