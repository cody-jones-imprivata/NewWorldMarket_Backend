from django.db import models

class Posts(models.Model):
    """GameUsers Model
    Fields:
        posterId (ForeignKey): the user that made the event
        item (ForeignKey): the game associated with the event
        settlementId (DateField): The date of the event
        description (CharField): : The text description of the event
    """
    poster  = models.ForeignKey("GameUsers", on_delete=models.CASCADE)
    item = models.ForeignKey("Items", on_delete=models.CASCADE)
    settlement = models.ForeignKey("Settlements", on_delete=models.CASCADE)
    description  = models.CharField(max_length=50)
    sold = models.BooleanField(null=True)

    
    @property
    def isMine(self):
        return self.__isMine

    @isMine.setter
    def isMine(self, value):
        self.__isMine = value

