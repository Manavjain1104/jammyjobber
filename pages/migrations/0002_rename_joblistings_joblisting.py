# Generated by Django 4.1 on 2024-01-18 15:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="JobListings",
            new_name="JobListing",
        ),
    ]
