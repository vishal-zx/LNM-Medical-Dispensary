# Generated by Django 3.2.7 on 2021-12-19 06:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20211218_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('Mid', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=50)),
                ('Type', models.CharField(max_length=50)),
                ('Quantity', models.IntegerField(default=1000)),
                ('Usage', models.IntegerField(default=0)),
                ('Supplier', models.CharField(max_length=30)),
                ('PurchaseDate', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('ExpiryDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='PatientHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Description', models.TextField()),
                ('Aid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.appointment')),
                ('Pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
            ],
        ),
    ]