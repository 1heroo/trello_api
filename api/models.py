from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from datetime import datetime


class MyUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=False, blank=True)
    email = models.EmailField(
        _("email address"),
        unique=True
    )
    code = models.CharField(max_length=10, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return f'{super().first_name} {super().last_name}'

    def set_code(self):
        code = get_random_string(10)
        self.code = code
        self.save()
        return code


class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    deadline = models.DateField()
    author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, related_name='one_author', blank=True)


class Comment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, related_name='users_comments')
    created_at = models.DateTimeField(default=datetime.now)
    text = models.TextField(max_length=1000)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='cards_comment')

    def __str__(self):
        return 'comment from {name} {last}'.format(name=self.author.first_name, last=self.author.last_name)

    class Meta:
        ordering = ['-created_at']


class Members(models.Model):
    user = models.ForeignKey(MyUser, related_name='members', on_delete=models.CASCADE)
    card = models.ForeignKey(Card, related_name='members', on_delete=models.CASCADE)


class Mark(models.Model):
    title = models.CharField(max_length=50)
    colour = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class MarkCard(models.Model):
    card = models.ForeignKey(Mark, on_delete=models.CASCADE, related_name='mark_cards')
    mark = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='card_marks')


class Column(models.Model):
    title = models.CharField(max_length=100, default='green')

    def __str__(self):
        return self.title


class ColumnCard(models.Model):
    columns = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='card_columns')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='column_cards')


class Board(models.Model):
    title = models.CharField(max_length=100)
    is_archived = models.BooleanField(default=False, blank=True, null=True)
    image = models.ImageField(upload_to='boards/', blank=True)

    def __str__(self):
        return self.title


class BoardColumn(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='column_boards')
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='board_columns')


class Image(models.Model):
    image = models.ImageField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="images")


class BoardMembers(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='member_boards')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='board_members')


class FavoriteBoard(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='users')
    board = models.ForeignKey(Board, on_delete=models.SET_NULL, blank=True, null=True, related_name='boards')

    def __str__(self):
        return self.board


