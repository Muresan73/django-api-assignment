# Generated by Django 4.1.3 on 2022-11-07 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_aggregator', '0004_link_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]