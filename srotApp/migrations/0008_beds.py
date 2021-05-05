# Generated by Django 3.1.7 on 2021-05-05 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srotApp', '0007_food'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_name', models.CharField(max_length=100)),
                ('hospital_contact', models.CharField(max_length=100)),
                ('hospital_city', models.CharField(max_length=100)),
                ('hospital_address', models.CharField(max_length=500)),
                ('hospital_beds', models.CharField(max_length=100)),
                ('hospital_verify', models.CharField(max_length=100)),
                ('hospital_details', models.CharField(max_length=500)),
            ],
        ),
    ]
