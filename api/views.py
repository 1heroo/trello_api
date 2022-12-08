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
from api.serializers import CardSerializer, CardGetSerializer


# Create your views here.
class CardAPIListCreate(APIView):

    def get(self, request):
        cards = Card.objects.all().values()
        return Response({'Data': list(cards)})

    @swagger_auto_schema(request_body=CardSerializer)
    def post(self, request):
        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CardAPIView(APIView):

    def get(self, request, pk):
        card = Card.objects.get(pk=pk)
        serializer = CardGetSerializer(card)
        return Response({"Data": serializer.data})