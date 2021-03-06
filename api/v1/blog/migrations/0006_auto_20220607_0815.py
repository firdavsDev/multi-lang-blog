# Generated by Django 3.2.6 on 2022-06-07 03:15

import django.db.models.deletion
import django.db.models.manager
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_auto_20220607_0743'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='blog',
            managers=[
                ('cus_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='blog',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_author', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='categories', to='blog.Category', verbose_name='categories'),
        ),
    ]
