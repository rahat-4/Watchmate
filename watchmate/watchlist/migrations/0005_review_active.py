# Generated by Django 4.1.2 on 2022-10-08 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0004_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
