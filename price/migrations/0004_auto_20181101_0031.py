# Generated by Django 2.1.2 on 2018-10-31 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0003_auto_20181101_0005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['mark', 'name', '-price']},
        ),
    ]
