"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from newworldapi.models import Posts, Items, GameUsers,Settlements,Servers


class ServerViewSet(ViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Servers.objects.none()
    def create(self, request):

        try:
            #new server being created
            server = Servers.objects.create(
                serverName=GameUsers.objects.get(pk=request.data['serverName']),
            )
            serializer = ServerSerializer(server, context={'request': request})
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
            server = Servers.objects.get(pk=pk)
            serializer = ServerSerializer(server, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk):
        server = Servers.objects.get(pk=pk)
        server.serverName = request.data['serverName']
        server.save()

        serializer = ServerSerializer(server, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        server = Servers.objects.all()

        servername = request.query_params.get('serverName', None)

        if servername is not None:
            server = server.filter(serverName=servername)

        serializer = ServerSerializer(
            server, many=True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            server = Servers.objects.get(pk=pk)
            server.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Servers.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servers
        fields = '__all__'
        # depth = 2