# Generated by Django 5.0.1 on 2024-03-24 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16, unique=True)),
                ('email', models.EmailField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('last_log', models.DateTimeField(auto_now=True)),
                ('mode', models.SmallIntegerField(default=0)),
            ],
            options={
                'db_table': 'user_login',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='user.user_login')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to='user.user_login')),
            ],
        ),
    ]