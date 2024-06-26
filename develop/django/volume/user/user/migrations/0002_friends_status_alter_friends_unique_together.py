# Generated by Django 5.0.1 on 2024-03-25 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='status',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='friends',
            unique_together={('user', 'friend')},
        ),
    ]
