# Generated by Django 3.1.5 on 2021-02-12 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dct', '0009_auto_20210212_0809'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accumulator',
            old_name='state',
            new_name='remark',
        ),
        migrations.RenameField(
            model_name='accumulatordate',
            old_name='remark',
            new_name='state',
        ),
    ]
