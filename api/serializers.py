from datetime import datetime
from rest_framework import serializers
from api.models import Comment, Column, Mark, MyUser, Board, Card, Members


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()


class CommentSerializer(serializers.Serializer):
    author_id = serializers.IntegerField()
    date = serializers.DateTimeField(default=datetime.now)
    text = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        user_id = validated_data.pop('author')
        user = MyUser.objects.get(pk=user_id)
        Comment.objects.create(author=user, **validated_data)
        return validated_data


class MarkSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    colour = serializers.CharField(max_length=300)


class CardRetrieveSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, required=False)
    description = serializers.CharField(max_length=1000, required=False)
    deadline = serializers.DateField(default=datetime.now, required=False)
    author = UserSerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        members = [member.user for member in instance.members.all()]
        marks = [mark.mark for mark in instance.card_marks.all()]
        comments = instance.cards_comment.all()

        representation['members'] = UserSerializer(members, many=True, context=self.context).data
        representation['marks'] = MarkSerializer(marks, many=True, context=self.context).data
        representation['comments'] = CommentSerializer(comments, many=True, context=self.context).data

        return representation


class CardSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, required=False)
    description = serializers.CharField(max_length=1000, required=False)
    deadline = serializers.DateField(default=datetime.now, required=False)
    author_id = serializers.IntegerField()

    def create(self, validated_data):
        Card.objects.create(**validated_data)
        return validated_data


class ColumnSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, default='green')

    def create(self, validated_data):
        Column.objects.create(**validated_data)
        return validated_data


class ColumnRetrieveSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        cards = [card.card for card in instance.card_columns.all()]
        representation['cards'] = CardSerializer(cards, many=True, context=self.context).data
        return representation


class BoardRetrieveSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    is_archived = serializers.BooleanField()
    image = serializers.ImageField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        members = [member.user for member in instance.member_boards.all()]
        columns = [column.column for column in instance.column_boards.all()]

        representation['members'] = UserSerializer(members, many=True, context=self.context).data
        representation['columns'] = ColumnSerializer(columns, many=True, context=self.context).data
        return representation


class BoardSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    is_archived = serializers.BooleanField()
    image = serializers.ImageField()

    def create(self, validated_data):
        Board.objects.create(**validated_data)
        return validated_data

