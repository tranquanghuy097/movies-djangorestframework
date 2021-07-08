from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=250)
    releasedate = models.DateField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name
