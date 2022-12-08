import datetime
from time import timezone
from rest_framework import serializers
from api.models import Comment, Column, Mark, MyUser, Board, Card, Members


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()


class MarkRetrieveSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    colour = serializers.CharField(max_length=300)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        cards = [card.card for card in instance.card_marks.all()]

        representation['cards'] = CardSerializer(cards, many=True, context=self.context).data
        return representation


class MarkSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False)
    colour = serializers.CharField(max_length=300, required=False)

    def create(self, validated_data):
        Mark.objects.create(**validated_data)
        return validated_data

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.colour = validated_data.get('colour', instance.colour)
        instance.save()
        return instance


class BoardRetrieveSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    is_archived = serializers.BooleanField()
    author = UserSerializer()
    image = serializers.ImageField(required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        members = [member.user for member in instance.member_boards.all()]
        columns = instance.column_boards.all()

        representation['members'] = UserSerializer(members, many=True, context=self.context).data
        representation['columns'] = ColumnSerializer(columns, many=True, context=self.context).data
        return representation


class BoardSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False)
    is_archived = serializers.BooleanField(required=False, default=False)
    author = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    image = serializers.ImageField(required=False)

    def create(self, validated_data):
        author = self.context.get('author')
        Board.objects.create(author=author, **validated_data)
        return validated_data

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.is_archived = validated_data.get('is_archived', instance.is_archived)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class ColumnSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, default='green', required=False)
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all(), required=False)

    def create(self, validated_data):
        Column.objects.create(**validated_data)
        return validated_data

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.board = validated_data.get('board', instance.board)

        instance.save()
        return instance


class ColumnRetrieveSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    board = BoardSerializer()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        cards = instance.cards.all()
        representation['cards'] = CardSerializer(cards, many=True, context=self.context).data
        return representation


class CardRetrieveSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, required=False)
    description = serializers.CharField(max_length=1000, required=False)
    deadline = serializers.DateField(read_only=True, required=False)
    column = ColumnSerializer()
    author = UserSerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        members = [member.user for member in instance.members.all()]
        marks = [mark.mark for mark in instance.mark_cards.all()]
        comments = instance.cards_comment.all()

        representation['members'] = UserSerializer(members, many=True, context=self.context).data
        representation['marks'] = MarkSerializer(marks, many=True, context=self.context).data
        representation['comments'] = CommentSerializer(comments, many=True, context=self.context).data

        return representation


class CardSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, required=False)
    description = serializers.CharField(max_length=1000, required=False)
    deadline = serializers.DateField(default=datetime.date.today, required=False)
    column = serializers.PrimaryKeyRelatedField(queryset=Column.objects.all())

    def create(self, validated_data):
        Card.objects.create(**validated_data)
        return validated_data

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.save()
        return instance


class CommentSerializer(serializers.Serializer):
    created_at = serializers.DateField(default=datetime.date.today)
    text = serializers.CharField(max_length=1000)
    card = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all())

    def create(self, validated_data):
        user = self.context.get('user')
        Comment.objects.create(author=user, **validated_data)
        return validated_data