from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Board, Column, Card, Mark
from rest_framework.parsers import MultiPartParser, FormParser

from api.permissions import BoardOwnerOrReadOnly, IsMemberOrBoardOwner
from .serializers import (CardSerializer, CardRetrieveSerializer,
                             ColumnSerializer, ColumnRetrieveSerializer,
                             BoardSerializer, BoardRetrieveSerializer,
                             CommentSerializer, MarkSerializer, MarkRetrieveSerializer)


class CommentAPIView(APIView):
    permission_classes = [IsMemberOrBoardOwner]

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request):
        card = Card.objects.get(pk=request.data.get('card'))
        self.check_object_permissions(request, card)
        serializer = CommentSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CardAPIListCreate(APIView):
    # permission_classes = [BoardOwnerOrReadOnly]

    def get(self, request):
        cards = Card.objects.all().values()
        return Response({'data': list(cards)})

    @swagger_auto_schema(request_body=CardSerializer)
    def post(self, request):
        column = Column.objects.get(pk=request.data.get('column'))
        self.check_object_permissions(request, column.board)

        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CardAPIView(APIView):
    permission_classes = [BoardOwnerOrReadOnly]

    def get_object(self, pk):
        return Card.objects.get(pk=pk)

    def get(self, request, pk):
        card = self.get_object(pk=pk)
        serializer = CardRetrieveSerializer(card)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CardSerializer)
    def put(self, request, pk):
        card = self.get_object(pk=pk)
        serializer = CardSerializer(instance=card, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CardSerializer)
    def patch(self, request, pk):
        card = self.get_object(pk=pk)
        serializer = CardSerializer(instance=card, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        card = self.get_object(pk=pk)
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ColumnAPIVListCreate(APIView):
    permission_classes = [BoardOwnerOrReadOnly]

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
    permission_classes = [BoardOwnerOrReadOnly]

    def get_object(self, pk):
        return Column.objects.get(pk=pk)

    def get(self, request, pk):
        column = self.get_object(pk=pk)
        serializer = ColumnRetrieveSerializer(column)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ColumnSerializer)
    def put(self, request, pk):
        column = self.get_object(pk=pk)
        serializer = ColumnSerializer(instance=column, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ColumnSerializer)
    def patch(self, request, pk):
        column = self.get_object(pk=pk)
        serializer = ColumnSerializer(instance=column, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        column = self.get_object(pk=pk)
        column.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BordAPIListCreate(APIView):
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards = Board.objects.all().values()
        return Response({'data': list(boards)}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BoardSerializer)
    def post(self, request):
        serializer = BoardSerializer(data=request.data, context={'author': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BoardAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)

    def get_object(self, pk):
        return Board.objects.get(pk=pk)

    def get(self, request, pk):
        board = self.get_object(pk=pk)
        serializer = BoardRetrieveSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BoardSerializer)
    def put(self, request, pk):
        board = self.get_object(pk=pk)
        serializer = BoardSerializer(instance=board, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BoardSerializer)
    def patch(self, request, pk):
        board = self.get_object(pk=pk)
        serializer = BoardSerializer(instance=board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        board = self.get_object(pk=pk)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MarkAPIView(APIView):

    def get_object(self, pk):
        return Mark.objects.get(pk=pk)

    def get(self, request, pk):
        mark = self.get_object(pk=pk)
        serializer = MarkRetrieveSerializer(mark)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=MarkSerializer)
    def put(self, request, pk):
        mark = self.get_object(pk=pk)
        serializer = MarkSerializer(instance=mark, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=MarkSerializer)
    def patch(self, request, pk):
        mark = self.get_object(pk=pk)
        serializer = MarkSerializer(instance=mark, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        mark = self.get_object(pk=pk)
        mark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MarkAPIListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        marks = Mark.objects.all().values()
        return Response({'data': list(marks)}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=MarkSerializer)
    def post(self, request):
        serializer = MarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



