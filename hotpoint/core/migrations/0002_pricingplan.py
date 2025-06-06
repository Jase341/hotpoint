# Generated by Django 4.2 on 2025-05-08 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PricingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(help_text='Amount in KES (e.g., 10, 20, 50)', unique=True)),
                ('duration_minutes', models.PositiveIntegerField(help_text='Duration in minutes (e.g., 30, 60, 180)')),
            ],
        ),
    ]
