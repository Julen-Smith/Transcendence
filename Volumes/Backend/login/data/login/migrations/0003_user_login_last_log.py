# Generated by Django 5.0.1 on 2024-02-02 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_login',
            name='last_log',
            field=models.DateField(auto_now=True),
        ),
    ]
