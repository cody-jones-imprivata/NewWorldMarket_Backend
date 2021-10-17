"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models.fields import BooleanField
from rest_framework import serializers
from django.db.models import Case, When
from newworldapi.models import Posts, Messages,GameUsers

"""
To do:
combine postviews and messageviews together

"""

class MessageViewSet(ViewSet):

    def create(self, request):
        """[summary]
        Args:
            request ([type]): [description]
        Returns:
            [type]: [description]
        """
        
        try:
            message = Messages.objects.create(
                sender=GameUsers.objects.get(user=request.auth.user.pk),
                receiver = GameUsers.objects.get(user=request.data['receiver']),
                post=Posts.objects.get(pk=request.data['post']),
                seen = request.data['seen'],
                message=request.data['message'],
            )
            serializer = MessageSerializer(message, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            message = Messages.objects.get(pk=pk)
            gameuser = GameUsers.objects.get(user=request.auth.user)

            if gameuser == message.sender or gameuser == message.receiver:
                message.isMine = True
            else:
                message.isMine = False

            serializer = MessageSerializer(message, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk):
        message = Messages.objects.get(pk=pk)
        message.message = request.data['message']
        message.seen = request.data['seen']
        message.save()

        serializer = MessageSerializer(message, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to posts"""
        gameuser = GameUsers.objects.get(user=request.auth.user)      
        post = request.query_params.get('post', None)
        if post is not None:
            messages = Messages.objects.filter(post=post)


        for message in messages:
            if gameuser == message.sender :
                message.isMine = True
                message.isMineSender = True
            else:
                message.isMine = False
                message.isMineSender = False

        for message in messages:
            if gameuser == message.receiver :
                message.isMine = True
                message.isMineReceiver = True
            else:
                message.isMine = False
                message.isMineReceiver = False
                
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)


    def destroy(self, request, pk):
        try:
            messages = Messages.objects.get(pk=pk)
            messages.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Posts.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'username','email','is_superuser']

class GameUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUsers"""
    user = UserSerializer(many=False)
    class Meta:
        model = GameUsers
        fields = ('id', 'user', 'inGamename', 'discord', 'faction','server')
        depth = 1

class MessageSerializer(serializers.ModelSerializer):
    sender = GameUserSerializer(many=False)
    receiver = GameUserSerializer(many=False)
    class Meta:
        model = Messages
        fields = ('id','message','sender','receiver','post','isMine','isMineSender','isMineReceiver')
        depth = 2