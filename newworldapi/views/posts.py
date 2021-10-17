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
        try:
            #new post being created
            post = Posts.objects.create(
                poster=GameUsers.objects.get(user=request.auth.user.pk),
                settlement=Settlements.objects.get(pk=request.data['settlement']),
                item=Items.objects.get(pk=request.data['item']),
                description=request.data['description'],
                sold= False
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
            post = Posts.objects.get(pk=pk)
            gameuser = GameUsers.objects.get(user=request.auth.user)

            if gameuser == post.poster:
                post.isMine = True
            else:
                post.isMine = False

            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk):

        try:
            post = Posts.objects.get(pk=pk)
            post.settlement = Settlements.objects.get(pk=request.data['settlement'])
            post.description = request.data['description']
            post.item = Items.objects.get(pk=request.data['item'])
            post.sold = request.data['sold']
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        posts = Posts.objects.all()
        soldQuery= request.query_params.get('sold', None)

        if soldQuery is not None:
            posts = posts.filter(sold=soldQuery)

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


class PostSerializer(serializers.ModelSerializer):
    poster = GameUserSerializer(many=False)
    class Meta:
        model = Posts
        fields = ('id','poster','isMine','item','settlement','description','sold')
        depth = 2