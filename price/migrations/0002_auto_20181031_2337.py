# Generated by Django 2.1.2 on 2018-10-31 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='mark',
            field=models.CharField(blank=True, max_length=200, verbose_name='Mark'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='item',
            name='pub_date',
            field=models.DateField(default='2018-10-31', verbose_name='date added'),
        ),
    ]
