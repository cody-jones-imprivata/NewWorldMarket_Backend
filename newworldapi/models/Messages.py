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
    post = models.ForeignKey("Posts", on_delete=models.CASCADE)
    sender = models.ForeignKey("GameUsers", on_delete=models.CASCADE)
    receiver = models.ForeignKey("GameUsers", on_delete=models.CASCADE,related_name='receiver',null=True)
    message  = models.CharField(max_length=50)
    seen = models.BooleanField()
    timeStamp= models.IntegerField(null=True) 

    @property
    def currentUser(self):
        return self.__currentUser

    @currentUser.setter
    def currentUser(self, value):
        self.__currentUser = value

