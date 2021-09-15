from django.db import models

class Items(models.Model):
    """GameUsers Model
    Fields:
        posterId (ForeignKey): the user that made the event
        item (ForeignKey): the game associated with the event
        settlementId (DateField): The date of the event
        time (TimeFIeld): The time of the event
        description (CharField): : The text description of the event
    """
    itemName  = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    rarity = models.CharField(max_length=50)
    tier  = models.CharField(max_length=50)
    link = models.CharField(max_length=50)
    image = models.CharField(max_length=50)
    
