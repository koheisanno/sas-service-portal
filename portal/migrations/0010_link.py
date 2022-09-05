# Generated by Django 3.2.4 on 2021-07-20 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_club_instagram'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('url', models.CharField(max_length=120)),
                ('category', models.CharField(choices=[('quick-links', 'Quick Links'), ('officers-only', 'Officers Only')], max_length=120)),
            ],
        ),
    ]
