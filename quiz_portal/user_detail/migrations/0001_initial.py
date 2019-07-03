# Generated by Django 2.2.2 on 2019-07-03 03:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('contact_num', models.IntegerField()),
                ('password', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('college', models.CharField(max_length=100)),
                ('events', models.ManyToManyField(to='events.Event')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
