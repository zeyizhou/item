# Generated by Django 2.1.2 on 2018-11-05 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0004_auto_20181101_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='pub_date',
            field=models.DateField(blank=True, default='2018-11-05', verbose_name='date added'),
        ),
    ]
