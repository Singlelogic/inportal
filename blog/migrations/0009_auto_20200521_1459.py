# Generated by Django 3.0.4 on 2020-05-21 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_image_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_preview',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
