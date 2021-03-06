# Generated by Django 3.0.4 on 2020-06-10 17:28

import blog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20200608_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_preview',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20)),
                ('image', models.ImageField(upload_to=blog.models.get_image_filename, verbose_name='Image')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
        ),
    ]
