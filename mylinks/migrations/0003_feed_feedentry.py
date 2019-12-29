# Generated by Django 2.2.4 on 2019-10-12 00:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mylinks.models.methods


class Migration(migrations.Migration):

    dependencies = [
        ('mylinks', '0002_auto_20190923_0852'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('title', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Feed Title')),
                ('url', models.URLField(unique=True, verbose_name='Feed URL')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Feed Link')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Feed Description')),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='Feed Published At')),
                ('last_polled_at', models.DateTimeField(blank=True, null=True, verbose_name='Feed Last Polled At')),
            ],
            options={
                'verbose_name': 'Feed',
                'verbose_name_plural': 'Feeds',
            },
            bases=(models.Model, mylinks.models.methods.Feed),
        ),
        migrations.CreateModel(
            name='FeedEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Feed Entry Description')),
                ('published_at', models.DateTimeField(auto_now_add=True, verbose_name='Feed Entry Published At')),
                ('is_read', models.BooleanField(default=False)),
                ('trashed', models.BooleanField(default=False)),
                ('feeds', models.ManyToManyField(blank=True, to='mylinks.Feed')),
                ('link', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mylinks.Link')),
            ],
            options={
                'verbose_name': 'Feed Entry',
                'verbose_name_plural': 'Feed Entries',
                'ordering': ['-published_at'],
            },
            bases=(models.Model, mylinks.models.methods.FeedEntry),
        ),
    ]