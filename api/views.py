from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import BoardOwnerOrReadOnly
from api.CRUD.serializers import BoardSerializer
from api.models import Board, MyUser, Mark
from api.serializers import (InviteToBoardSerializer,
                             AddToCardSerializer, FavouriteBoardSerializer,
                             RemoveFavouriteSerializer, ArchivingSerializer, MarkACardSerializer, UnMarkACardSerializer)


class InviteMemberToBoardView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=InviteToBoardSerializer)
    def post(self, request):
        serializer = InviteToBoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AddToMemberCard(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AddToCardSerializer)
    def post(self, request):
        serializer = AddToCardSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FavouriteBoardsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards = [board.board for board in request.user.users_faves.all()]
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=FavouriteBoardSerializer)
    def post(self, request):
        serializer = FavouriteBoardSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=RemoveFavouriteSerializer)
    def delete(self, request):
        serialize = RemoveFavouriteSerializer(context={'user': request.user})
        serialize.save(data=request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArchivingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards = Board.objects.filter(is_archived=True, author=request.user)
        self.check_permissions(request=request)
        return Response(list(boards.values()), status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ArchivingSerializer)
    def post(self, request):
        board = Board.objects.get(pk=request.data['board'])

        serializer = BoardSerializer(instance=board, data={'is_archived': True})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ArchivingSerializer)
    def delete(self, request):
        board = Board.objects.get(pk=request.data['board'])
        self.check_object_permissions(request=request, obj=board)

        serializer = BoardSerializer(instance=board, data={'is_archived': False})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, query):
        queryset = MyUser.objects.filter(first_name__icontains=query) or \
                   MyUser.objects.filter(last_name__icontains=query) or \
                   Mark.objects.filter(title__icontains=query)

        return Response(list(queryset.values()), status=status.HTTP_200_OK)


class MarkACard(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=MarkACardSerializer)
    def post(self, request):
        serializer = MarkACardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=UnMarkACardSerializer)
    def delete(self, request):
        serializer = UnMarkACardSerializer()
        serializer.save(data=request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)