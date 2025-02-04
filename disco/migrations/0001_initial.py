# Generated by Django 5.1.4 on 2024-12-07 23:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('providers', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(null=True)),
                ('arrived_at', models.DateTimeField(null=True)),
                ('booking_id', models.CharField(max_length=255)),
                ('cancel_reason', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('distance', models.FloatField(null=True)),
                ('estimated_fare', models.JSONField(null=True)),
                ('estimated_travel_time_in_mins', models.FloatField()),
                ('final_fare', models.JSONField(null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('is_airport', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('pink_whip', models.BooleanField(default=False)),
                ('provider_rating', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('surge', models.BooleanField(null=True)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('toll_amount', models.FloatField(blank=True, null=True)),
                ('travel_time_in_mins', models.FloatField(null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('user_rating', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('waiting_time_in_minutes', models.IntegerField(null=True)),
                ('vehicle_type', models.CharField(max_length=255, null=True)),
                ('platform_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('cancelled_at', models.DateTimeField(blank=True, null=True)),
                ('airport_code', models.CharField(max_length=255, null=True)),
                ('destination_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ride_destination_location', to='users.locations')),
                ('provider_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provider_rides', to='providers.providerprofile')),
                ('source_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ride_source_location', to='users.locations')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rides', to='users.userprofile')),
            ],
            options={
                'db_table': 'rides',
            },
        ),
    ]
