# Generated by Django 4.0.4 on 2022-06-06 13:25

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blog_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postlanguage',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='content'),
        ),
    ]
