"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from newworldapi.models import Items,GameUsers


class ItemViewSet(ViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Items.objects.none()
    def create(self, request):

        try:
            #new item being created
            item = Items.objects.create(
                itemName=request.data['itemName'],
                type=request.data['type'],
                rarity=request.data['rarity'],
                tier=request.data['tier'],
                link = request.data['link'],
                image = request.data['image']
            )
            serializer = ItemSerializer(item, context={'request': request})
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
            #   http://localhost:8000/items/2
            #
            # The `2` at the end of the route becomes `pk`
            item = Items.objects.get(pk=pk)
            serializer = ItemSerializer(item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk):
        item = Items.objects.get(pk=pk)
        item.itemName=request.data['itemName'],
        item.type=request.data['type'],
        item.rarity=request.data['rarity'],
        item.tier=request.data['tier'],
        item.link = request.data['link'],
        item.image = request.data['image']
        item.save()

        serializer = ItemSerializer(item, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        item = Items.objects.all()

        itemname = request.query_params.get('itemName', None)
        rarity = request.query_params.get('rarity', None)
        tier = request.query_params.get('tier', None)
        type = request.query_params.get('type', None)


        if itemname is not None:
            item = item.filter(itemName=itemname)
        if rarity is not None:
            item = item.filter(rarity=rarity) 
        if tier is not None:
            item = item.filter(tier=tier) 
        if type is not None:
            item = item.filter(type=type) 
            
        serializer = ItemSerializer(
            item, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            item = Items.objects.get(pk=pk)
            item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Items.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'
        # depth = 2