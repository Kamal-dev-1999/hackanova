# Generated by Django 4.1.13 on 2025-02-21 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_excelfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
    ]
