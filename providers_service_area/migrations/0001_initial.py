# Generated by Django 4.1.4 on 2022-12-10 23:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=250, validators=[django.core.validators.RegexValidator(message='Non-valid Phone Number', regex='^\\+?\\d{8,17}$')])),
                ('language', models.CharField(max_length=50)),
                ('currency', models.CharField(max_length=50)),
            ],
        ),
    ]
