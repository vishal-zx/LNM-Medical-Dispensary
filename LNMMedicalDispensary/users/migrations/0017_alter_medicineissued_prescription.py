# Generated by Django 3.2.8 on 2021-12-21 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20211221_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicineissued',
            name='prescription',
            field=models.CharField(max_length=500),
        ),
    ]
