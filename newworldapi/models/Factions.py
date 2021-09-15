from django.db import models

class Factions(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    factionName = models.CharField(max_length=50)
