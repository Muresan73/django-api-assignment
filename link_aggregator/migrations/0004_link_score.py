# Generated by Django 4.1.3 on 2022-11-07 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_aggregator', '0003_alter_link_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]