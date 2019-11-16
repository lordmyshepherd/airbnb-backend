# Generated by Django 2.2.7 on 2019-11-14 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'amenities',
            },
        ),
        migrations.CreateModel(
            name='Beds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bed_type', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'beds',
            },
        ),
        migrations.CreateModel(
            name='RefundPolicies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=1000)),
            ],
            options={
                'db_table': 'refund_policies',
            },
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('number_of_persons', models.IntegerField()),
                ('number_of_baths', models.IntegerField()),
                ('description', models.TextField(max_length=3000)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'rooms',
            },
        ),
        migrations.CreateModel(
            name='RoomTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'room_types',
            },
        ),
        migrations.CreateModel(
            name='Rules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'rules',
            },
        ),
        migrations.CreateModel(
            name='RoomsRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Rooms')),
                ('rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Rules')),
            ],
            options={
                'db_table': 'rooms_to_rules',
            },
        ),
        migrations.CreateModel(
            name='RoomsBeds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_beds', models.IntegerField()),
                ('bed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Beds')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Rooms')),
            ],
            options={
                'db_table': 'rooms_to_beds',
            },
        ),
        migrations.CreateModel(
            name='RoomsAmenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Amenities')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Rooms')),
            ],
            options={
                'db_table': 'rooms_to_amenities',
            },
        ),
        migrations.AddField(
            model_name='rooms',
            name='amenity',
            field=models.ManyToManyField(through='rooms.RoomsAmenities', to='rooms.Amenities'),
        ),
        migrations.AddField(
            model_name='rooms',
            name='bed',
            field=models.ManyToManyField(through='rooms.RoomsBeds', to='rooms.Beds'),
        ),
        migrations.AddField(
            model_name='rooms',
            name='refund_policy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.RefundPolicies'),
        ),
        migrations.AddField(
            model_name='rooms',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.RoomTypes'),
        ),
        migrations.AddField(
            model_name='rooms',
            name='rules',
            field=models.ManyToManyField(through='rooms.RoomsRules', to='rooms.Rules'),
        ),
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.URLField(max_length=500)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Rooms')),
            ],
            options={
                'db_table': 'pictures',
            },
        ),
    ]
