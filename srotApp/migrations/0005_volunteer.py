# Generated by Django 3.1.7 on 2021-05-17 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srotApp', '0004_auto_20210517_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volunteer_name', models.CharField(max_length=100)),
                ('volunteer_email', models.CharField(max_length=100)),
                ('volunteer_age', models.CharField(max_length=100)),
                ('volunteer_phone', models.CharField(max_length=100)),
                ('volunteer_hours', models.CharField(max_length=100)),
                ('volunteer_aadhar', models.CharField(max_length=100)),
                ('volunteer_why', models.CharField(max_length=5000)),
            ],
        ),
    ]
