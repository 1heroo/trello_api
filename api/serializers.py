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


class CardGetSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, required=False)
    description = serializers.CharField(max_length=1000, required=False)
    deadline = serializers.DateField(default=datetime.now, required=False)
    author = UserSerializer(read_only=True)
    # members = serializers.PrimaryKeyRelatedField(read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        members = [member.user for member in Members.objects.filter(card=instance)]
        repr['members'] = UserSerializer(members, many=True, context=self.context).data
        repr['comments'] = CommentSerializer()
        return repr


class CardSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, required=False)
    description = serializers.CharField(max_length=1000, required=False)
    deadline = serializers.DateField(default=datetime.now, required=False)
    author_id = serializers.IntegerField()

    def create(self, validated_data):
        Card.objects.create(**validated_data)
        return validated_data

    def to_representation(self, instance):
        reps = super().to_representation(instance)
        if instance.comments.exists():
            reps['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return reps

