# Generated by Django 3.1.5 on 2021-04-01 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dct', '0002_auto_20210309_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='accumulator',
            name='date_purchase',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата закупки'),
        ),
    ]
