# Generated by Django 3.1.5 on 2021-02-11 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Пользователь')),
            ],
        ),
    ]