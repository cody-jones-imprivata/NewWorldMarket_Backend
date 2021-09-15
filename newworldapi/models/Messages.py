from django.db import models

class Messages(models.Model):
    """GameUsers Model
    Fields:
        posterId (ForeignKey): the user that made the event
        item (ForeignKey): the game associated with the event
        settlementId (DateField): The date of the event
        time (TimeFIeld): The time of the event
        description (CharField): : The text description of the event
    """
    posterUserid  = models.ForeignKey("Posts", on_delete=models.CASCADE,related_name='PostUserId')
    postId = models.ForeignKey("Posts", on_delete=models.CASCADE)
    userId = models.ForeignKey("GameUsers", on_delete=models.CASCADE)
    message  = models.CharField(max_length=50)
    seen = models.BooleanField()
    timeStamp= models.IntegerField(null=True) 
