# Generated by Django 3.1.5 on 2021-02-16 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dct', '0011_auto_20210212_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataCollectTerminalRemark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('data_collect_terminal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dct.datacollectterminal')),
            ],
        ),
    ]