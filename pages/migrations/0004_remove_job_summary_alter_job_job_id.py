# Generated by Django 5.0.1 on 2024-02-18 15:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0003_cv_job_delete_joblisting"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="job",
            name="summary",
        ),
        migrations.AlterField(
            model_name="job",
            name="job_id",
            field=models.CharField(max_length=255),
        ),
    ]
