from django.db import models

class GameUsers(models.Model):

    settlementName = models.CharField(max_length=50)
    