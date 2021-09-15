"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from newworldapi.models import Posts, Items, GameUsers,Settlements


class PostViewSet(ViewSet):

    def create(self, request):
        """[summary]
        Args:
            request ([type]): [description]
        Returns:
            [type]: [description]
        """
        Poster = User.objects.get(user=request.auth.user)
        Settlement = Settlements.objects.get(pk=request.data['SettlementId'])
        Item = Items.objects.get(pk=request.data['ItemId'])
        try:
            post = Posts.objects.create(
                posterId=Poster,
                settlementId=Settlement,
                item=Item,
                description=request.data['description'],
                TimeStamp=request.data['timeStamp'],
            )
            serializer = PostSerializer(post, context={'request': request})
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
            post = Posts.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk):
        post = Posts.objects.get(pk=pk)
        post.settlementId = Settlements.objects.get(pk=request.data['SettlementId'])
        post.description = request.data['skill_level']
        post.item = Items.objects.get(pk=request.data['ItemId'])
        post.save()

        serializer = PostSerializer(post, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        posts = Posts.objects.all()

        settlement = request.query_params.get('settlementid', None)

        if settlement is not None:
            posts = posts.filter(game_type__id=settlement)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            post = Posts.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Posts.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'
        # depth = 2