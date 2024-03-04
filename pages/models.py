from django.db import models


# Create your models here.
class Job(models.Model):
    job_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    is_significant = models.BooleanField(default=False)
    # summary = models.TextField()
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    def significant(self):
        self.is_significant = True


class CV(models.Model):
    pdf = models.FileField()

    def __str__(self):
        return self.title
