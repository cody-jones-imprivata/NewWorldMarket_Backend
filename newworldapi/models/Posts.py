from django.db import models

class Posts(models.Model):
    """GameUsers Model
    Fields:
        posterId (ForeignKey): the user that made the event
        item (ForeignKey): the game associated with the event
        settlementId (DateField): The date of the event
        time (TimeFIeld): The time of the event
        description (CharField): : The text description of the event
    """
    posterId  = models.ForeignKey("GameUsers", on_delete=models.CASCADE)
    item = models.ForeignKey("Items", on_delete=models.CASCADE)
    settlementId = models.ForeignKey("Settlements", on_delete=models.CASCADE)
    description  = models.CharField(max_length=50)
    timeStamp = models.IntegerField() 

    @property
    def isMine(self):
        return self.__isMine

    @isMine.setter
    def isMine(self, value):
        self.__isMine = value

