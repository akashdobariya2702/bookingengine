# Generated by Django 3.2 on 2021-11-06 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('hotel_room', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to='listings.hotelroom')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to='listings.listing')),
            ],
        ),
    ]
