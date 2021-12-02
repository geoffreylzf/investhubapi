# Generated by Django 3.2.9 on 2021-11-30 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('article', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='topics', to='core.article')),
                ('created_by', models.ForeignKey(db_column='created_by', db_constraint=False, default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='articletopic_create_related', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(db_column='deleted_by', db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='articletopic_delete_related', to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='articletopic_related', to='core.topic')),
                ('updated_by', models.ForeignKey(db_column='updated_by', db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='articletopic_update_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'article_topic',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ArticleStockCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('article', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='stock_counters', to='core.article')),
                ('created_by', models.ForeignKey(db_column='created_by', db_constraint=False, default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='articlestockcounter_create_related', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(db_column='deleted_by', db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='articlestockcounter_delete_related', to=settings.AUTH_USER_MODEL)),
                ('stock_counter', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='articlestockcounter_related', to='core.stockcounter')),
                ('updated_by', models.ForeignKey(db_column='updated_by', db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='articlestockcounter_update_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'article_stock_counter',
                'ordering': ['id'],
            },
        ),
    ]