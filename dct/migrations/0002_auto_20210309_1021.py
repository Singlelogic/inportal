# Generated by Django 3.1.5 on 2021-03-09 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dct', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accumulator',
            options={'ordering': ['number'], 'verbose_name': 'Аккумулятор', 'verbose_name_plural': 'Аккумуляторы'},
        ),
        migrations.AlterModelOptions(
            name='accumulatordate',
            options={'ordering': ['date']},
        ),
        migrations.AlterModelOptions(
            name='datacollectterminalremark',
            options={'ordering': ['-date'], 'verbose_name': 'Примечание', 'verbose_name_plural': 'Примечания'},
        ),
    ]