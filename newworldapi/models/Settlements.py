from django.db import models

class Settlements(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    settlementName = models.CharField(max_length=50)
    