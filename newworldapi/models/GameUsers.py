from django.db import models
from django.contrib.auth.models import User


class GameUsers(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    inGamename = models.CharField(max_length=50)
    discord = models.CharField(max_length=50)
    faction  = models.ForeignKey("Factions", on_delete=models.CASCADE)
    server  = models.ForeignKey("Servers", on_delete=models.CASCADE)
