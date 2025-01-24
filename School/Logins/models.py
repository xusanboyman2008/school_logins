from django.db import models

# Create your models here.
class Logins(models.Model):
    id=models.AutoField(primary_key=True)
    login=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    status=models.BooleanField(default=True)

class User(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    tg_id=models.IntegerField(null=False,blank=False)
    sending=models.BooleanField(default=False)