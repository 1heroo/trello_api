from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import (
    Board,
    Column,
    Card,
    Mark,
    Comment
)
from rest_framework.parsers import MultiPartParser, FormParser

from api.serializers import (CardSerializer, CardRetrieveSerializer,
                             ColumnSerializer, ColumnRetrieveSerializer, BoardSerializer, BoardRetrieveSerializer)


# Create your views here.
class CardAPIListCreate(APIView):

    def get(self, request):
        cards = Card.objects.all().values()
        return Response({'data': list(cards)})

    @swagger_auto_schema(request_body=CardSerializer)
    def post(self, request):
        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CardAPIView(APIView):

    def get(self, request, pk):
        card = Card.objects.get(pk=pk)
        serializer = CardRetrieveSerializer(card)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ColumnAPIVListCreate(APIView):

    def get(self, request):
        columns = Column.objects.all().values()
        return Response({'data': list(columns)}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ColumnSerializer)
    def post(self, request):
        serializer = ColumnSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ColumnAPIView(APIView):

    def get(self, request, pk):
        column = Column.objects.get(pk=pk)
        serializer = ColumnRetrieveSerializer(column)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BordAPIListCreate(APIView):
    parser_classes = (FormParser, MultiPartParser)

    def get(self, request):
        boards = Board.objects.all().values()
        return Response({'data': list(boards)}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BoardSerializer)
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BoardAPIView(APIView):

    def get(self, request, pk):
        board = Board.objects.get(pk=pk)
        serializer = BoardRetrieveSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)
