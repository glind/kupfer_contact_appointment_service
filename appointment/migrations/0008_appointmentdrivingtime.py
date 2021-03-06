# Generated by Django 2.2.1 on 2019-06-19 07:29

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0007_appointment_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentDrivingTime',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('distance', models.DecimalField(blank=True, decimal_places=2, help_text='Distance in predefined unit, p.e.: km', max_digits=5)),
                ('time', models.PositiveSmallIntegerField(blank=True, help_text='driving time in minutes')),
                ('time_point', models.DateTimeField(blank=True, help_text='Point in time when the driving took place', null=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driving_times', to='appointment.Appointment')),
            ],
        ),
    ]
