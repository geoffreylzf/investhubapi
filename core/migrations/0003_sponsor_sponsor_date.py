# Generated by Django 3.2.9 on 2021-12-14 10:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_sponsor'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='sponsor_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
