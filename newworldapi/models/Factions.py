from django.db import models

class GameUsers(models.Model):

    factionName = models.CharField(max_length=50)
