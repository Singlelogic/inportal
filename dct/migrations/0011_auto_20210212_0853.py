# Generated by Django 3.1.5 on 2021-02-12 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dct', '0010_auto_20210212_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accumulatordate',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата'),
        ),
    ]