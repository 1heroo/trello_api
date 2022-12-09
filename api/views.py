from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.CRUD.serializers import BoardSerializer
from api.models import Board
from api.serializers import InviteToBoardSerializer, InviteToCardSerializer, FavesSerializer, RemoveFaveSerializer, \
    ArchivingSerializer


class InviteMemberToBoardView(APIView):
    @swagger_auto_schema(request_body=InviteToBoardSerializer)
    def post(self, request):
        serializer = InviteToBoardSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InviteToCard(APIView):

    @swagger_auto_schema(request_body=InviteToCardSerializer)
    def post(self, request):
        serializer = InviteToCardSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AddToFaves(APIView):

    @swagger_auto_schema(request_body=FavesSerializer)
    def post(self, request):
        serializer = FavesSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=RemoveFaveSerializer)
    def delete(self, request):
        serialize = RemoveFaveSerializer(context={'user': request.user})
        serialize.save(data=request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArchivingView(APIView):

    @swagger_auto_schema(request_body=ArchivingSerializer)
    def post(self, request):
        board = Board.objects.get(pk=request.data['board'])
        if board.author == request.user:
            serializer = BoardSerializer(instance=board, data={'is_archived': True})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Only board author can archive board', status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(request_body=ArchivingSerializer)
    def patch(self, request):
        board = Board.objects.get(pk=request.data['board'])
        if board.author == request.user:
            serializer = BoardSerializer(instance=board, data={'is_archived': False})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Only board author can archive board', status=status.HTTP_403_FORBIDDEN)
