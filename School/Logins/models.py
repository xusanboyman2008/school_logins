from django.db import models


# Create your models here.
class Logins_model(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.login
    class Meta:
        ordering = ['id']


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tg_id = models.BigIntegerField()
    role = models.CharField(max_length=100,default="user")
    sending = models.BooleanField(default=False)
    def __str__(self):
        return self.name
