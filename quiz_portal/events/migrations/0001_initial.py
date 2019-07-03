# Generated by Django 2.2.2 on 2019-07-03 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100)),
                ('event_description', models.TextField()),
                ('event_url', models.URLField(blank=True, max_length=100)),
            ],
        ),
    ]
