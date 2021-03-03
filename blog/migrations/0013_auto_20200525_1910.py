# Generated by Django 3.0.4 on 2020-05-25 16:10

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200523_2112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='title',
        ),
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(upload_to=blog.models.get_image_filename, verbose_name='Image'),
        ),
    ]