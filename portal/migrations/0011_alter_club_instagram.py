# Generated by Django 3.2.4 on 2021-07-27 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0010_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='instagram',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
