# Generated by Django 2.0.1 on 2018-02-01 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20180131_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
