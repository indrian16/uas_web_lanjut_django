from django.db import models
from django.contrib.auth.models import User

class Biodata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=14)

    def __str__(self):
        return "{} - {} - {}".format(self.user, self.address, self.phone)

class API(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255)
