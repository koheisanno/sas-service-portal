# Generated by Django 3.2.4 on 2021-07-04 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos/'),
        ),
        migrations.AlterField(
            model_name='club',
            name='description',
            field=models.CharField(max_length=1200),
        ),
        migrations.AlterField(
            model_name='club',
            name='involvement',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='club',
            name='meeting',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='club',
            name='mission',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]
