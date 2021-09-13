from django.db import models

class GameUsers(models.Model):

    ServerName = models.CharField(max_length=50)
