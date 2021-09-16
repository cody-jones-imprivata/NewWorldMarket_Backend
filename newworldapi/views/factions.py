"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from newworldapi.models import Factions
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.permissions import DjangoModelPermissions

"""
To do:
combine postviews and messageviews together

"""

class FactionViewSet(ViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Factions.objects.none()
    def create(self, request):
        """[summary]
        Args:
            request ([type]): [description]
        Returns:
            [type]: [description]
        """
        try:
            faction = Factions.objects.create(
                factionName = request.data['factionName']
            )
            serializer = FactionSerializer(faction, context={'request': request})
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
            faction = Factions.objects.get(pk=pk)
            serializer = FactionSerializer(faction, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk):
        faction = Factions.objects.get(pk=pk)
        faction.factionName = request.data['factionName']
        faction.save()

        serializer = FactionSerializer(faction, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        factions = Factions.objects.all()

        factionName = request.query_params.get('factionName', None)

        if factionName is not None:
            factions = factions.filter(factionName=factionName)

        serializer = FactionSerializer(
            factions, many=True, context={'request': request})

        return Response(serializer.data)
        
    def destroy(self, request, pk):
        try:
            factions = Factions.objects.get(pk=pk)
            factions.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Factions.DoesNotExist as ex:
            return Response({'Faction': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'Faction': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factions
        fields = '__all__'
        # depth = 2