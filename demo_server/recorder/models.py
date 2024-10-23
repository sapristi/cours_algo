from django.db import models
# Create your models here.

class Record(models.Model):
    scheme = models.CharField(max_length=10)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=200)
    parameters = models.JSONField()
    body = models.TextField()
    headers = models.JSONField()
