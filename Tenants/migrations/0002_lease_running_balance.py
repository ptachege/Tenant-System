# Generated by Django 3.1.7 on 2021-07-04 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tenants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lease',
            name='running_balance',
            field=models.FloatField(default=0),
        ),
    ]
