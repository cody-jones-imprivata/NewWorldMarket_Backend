from django.db import models

class Messages(models.Model):
    """GameUsers Model
    Fields:
        posterId (ForeignKey): the user that made the event
        item (ForeignKey): the game associated with the event
        settlementId (DateField): The date of the event
        timeStamp (IntegerField): The time of the event
        description (CharField): : The text description of the event
    """
    post = models.ForeignKey("Posts", on_delete=models.CASCADE)
    sender = models.ForeignKey("GameUsers", on_delete=models.CASCADE)
    receiver = models.ForeignKey("GameUsers", on_delete=models.CASCADE,related_name='receiver',null=True)
    message  = models.CharField(max_length=50)
    seen = models.BooleanField()

    @property
    def isMine(self):
        return self.__isMine

    @isMine.setter
    def isMine(self, value):
        self.__isMine = value

    @property
    def isMineSender(self):
        return self.__isMineSender

    @isMineSender.setter
    def isMineSender(self, value):
        self.__isMineSender = value

    @property
    def isMineReceiver(self):
        return self.__isMineReceiver

    @isMineReceiver.setter
    def isMineReceiver(self, value):
        self.__isMineReceiver = value