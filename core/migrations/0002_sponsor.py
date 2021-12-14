# Generated by Django 3.2.9 on 2021-12-14 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('commission_pct', models.IntegerField(default=70)),
                ('amt', models.DecimalField(decimal_places=2, max_digits=15)),
                ('payment_type', models.CharField(max_length=20)),
                ('reference_no', models.CharField(max_length=500)),
                ('article', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sponsors', to='core.article')),
                ('created_by', models.ForeignKey(db_column='created_by', db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sponsor_create_related', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(db_column='deleted_by', db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sponsor_delete_related', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(db_column='updated_by', db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sponsor_update_related', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sponsors', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'sponsor',
                'ordering': ['id'],
            },
        ),
    ]
