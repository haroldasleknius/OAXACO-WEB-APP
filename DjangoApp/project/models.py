from django.db import models

class addModle(models.Model):
    photo = models.ImageField(upload_to='images/')