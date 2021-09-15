from django.db import models

class Servers(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    serverName = models.CharField(max_length=50)
