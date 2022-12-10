from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from api.models import BoardMembers, Members, Card, FavouriteBoards
from api.models import Board, MyUser
from api.utils import send_invitation_email


class InviteToBoardSerializer(serializers.Serializer):
    email = serializers.EmailField()
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())

    def create(self, validated_data):
        email = validated_data.get('email')
        board = validated_data.get('board')
        try:
            user = MyUser.objects.get(email=email)
            BoardMembers.objects.create(user=user, board=board)
        except ObjectDoesNotExist:
            send_invitation_email(email, board)
        return validated_data


class AddToCardSerializer(serializers.Serializer):
    email = serializers.EmailField()
    card = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all())

    def create(self, validated_data):
        board = validated_data.get('board')
        user = MyUser.objects.get(email=validated_data.get('email'))
        Members.objects.create(user=user, board=board)
        return validated_data


class FavouriteBoardSerializer(serializers.Serializer):
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())

    def create(self, validated_data):
        user = self.context.get('user')
        FavouriteBoards.objects.create(user=user,
                                       board=validated_data.get('board'))
        return validated_data


class RemoveFavouriteSerializer(serializers.Serializer):
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())

    def save(self, data):
        board = data.get('board')
        user = self.context.get('user')

        favour_board = user.users_faves.filter(board=board)
        favour_board.delete()
        return data


class ArchivingSerializer(serializers.Serializer):
    # uses only for swagger schema
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
