from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=250)
    age = models.IntegerField()
    gender = models.BinaryField()
    email = models.CharField(max_length=250)
    rating = models.FloatField()
    money = models.FloatField()

    def __str__(self):
        return self.name


class Job(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=250)
    job_description = models.TextField()
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.job_title
