# Generated by Django 3.2.9 on 2021-12-15 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorwithdraw',
            name='flow_status',
            field=models.ForeignKey(db_constraint=False, default=100, on_delete=django.db.models.deletion.DO_NOTHING, related_name='authorwithdraw_related', to='core.flowstatus'),
        ),
    ]