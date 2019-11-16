# Generated by Django 2.2.7 on 2019-11-17 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_auto_20191117_0756'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rooms',
            old_name='number_of_baths',
            new_name='bathroom',
        ),
        migrations.RenameField(
            model_name='rooms',
            old_name='number_of_persons',
            new_name='person_limit',
        ),
        migrations.AlterField(
            model_name='rooms',
            name='cleaning_fee',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='fee',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
    ]
