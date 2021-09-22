"""View module for handling requests about games"""
from newworldapi.models.Factions import Factions
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from newworldapi.models import GameUsers

"""
To do:
combine postviews and messageviews together

"""

class GameusersViewSet(ViewSet):

    def destroy(self, request, pk):
        try:
            gameuser = GameUsers.objects.get(pk=pk)
            gameuser.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except GameUsers.DoesNotExist as ex:
            return Response({'GameUsers': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'GameUsers': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            gameuser = GameUsers.objects.get(pk=pk)

            gameuser = GameUserSerializer(
            gameuser, many=False, context={'request': request})

            # Manually construct the JSON structure you want in the response
            profile = {}
            profile["gameuser"] = gameuser.data

            return Response(profile)

        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        GameUser = GameUsers.objects.all()

        inGamename = request.query_params.get('inGamename', None)

        if inGamename is not None:
            GameUser = GameUser.filter(inGamename=inGamename)

        serializer = GameUserSerializer(
            GameUser, many=True, context={'request': request})

        return Response(serializer.data)
  
class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for rareUser's related Django user"""
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'username')


class GameUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUsers"""
    user = UserSerializer(many=False)
    class Meta:
        model = GameUsers
        fields = ('id', 'user', 'inGamename', 'discord', 'faction','server')
        depth = 1
