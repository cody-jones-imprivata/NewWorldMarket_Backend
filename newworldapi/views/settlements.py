"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from newworldapi.models import Settlements
from rest_framework.permissions import DjangoModelPermissions

"""
To do:
combine postviews and messageviews together

"""

class SettlementViewSet(ViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Settlements.objects.none()
    def create(self, request):
        """[summary]
        Args:
            request ([type]): [description]
        Returns:
            [type]: [description]
        """
        try:
            settlement = Settlements.objects.create(
                settlementName = request.data['settlementName']
            )
            serializer = SettlementSerializer(settlement, context={'request': request})
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
            settlement = Settlements.objects.get(pk=pk)
            serializer = SettlementSerializer(settlement, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk):
        settlement = Settlements.objects.get(pk=pk)
        settlement.settlementName = request.data['settlementName']
        settlement.save()

        serializer = SettlementSerializer(settlement, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        settlements = Settlements.objects.all()

        settlementName = request.query_params.get('settlementName', None)

        if settlementName is not None:
            settlements = settlements.filter(settlementName=settlementName)

        serializer = SettlementSerializer(
            settlements, many=True, context={'request': request})

        return Response(serializer.data)
        
    def destroy(self, request, pk):
        try:
            settlements = Settlements.objects.get(pk=pk)
            settlements.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Settlements.DoesNotExist as ex:
            return Response({'Settlement': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'Settlement': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlements
        fields = '__all__'
        # depth = 2