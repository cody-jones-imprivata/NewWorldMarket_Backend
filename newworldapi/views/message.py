"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from newworldapi.models import Posts, Messages

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
        userId = User.objects.get(user=request.auth.user)
        postId = Posts.objects.get(pk=request.data['postId'])
        posterUserid = Posts.objects.get(pk=request.data['postUserid'])
        try:
            message = Messages.objects.create(
                posterUserid=posterUserid,
                userId=userId,
                postId=postId,
                seen = request.data['seen'],
                message=request.data['message'],
                TimeStamp=request.data['timeStamp'],
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
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            message = Messages.objects.get(pk=pk)
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
        messages = Messages.objects.all()

        postId = request.query_params.get('postId', None)

        if postId is not None:
            messages = messages.filter(postId=postId)

        serializer = MessageSerializer(
            messages, many=True, context={'request': request})

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


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
        # depth = 2