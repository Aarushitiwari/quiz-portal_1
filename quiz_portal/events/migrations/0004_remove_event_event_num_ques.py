# Generated by Django 2.2.2 on 2019-07-16 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20190715_0759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_num_ques',
        ),
    ]
