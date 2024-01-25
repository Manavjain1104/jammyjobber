from django.db import models


# Create your models here.
class Job(models.Model):
    job_id = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    summary = models.TextField()
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class CV(models.Model):
    pdf = models.FileField()

    def __str__(self):
        return self.title
