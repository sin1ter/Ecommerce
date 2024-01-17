# Generated by Django 4.2.8 on 2024-01-11 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_category_condition_met_alter_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='condition_met',
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
    ]
