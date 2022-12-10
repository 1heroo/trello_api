from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
import datetime


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


class Board(models.Model):
    title = models.CharField(max_length=100)
    is_archived = models.BooleanField(default=False)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='users_boards')
    image = models.ImageField(upload_to='images/%Y/%m/%d/')

    def __str__(self):
        return self.title


class BoardMembers(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='member_boards')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='board_members')


class Column(models.Model):
    title = models.CharField(max_length=100, default='green')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='column_boards')

    def __str__(self):
        return self.title


class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    deadline = models.DateField(default=datetime.date.today)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='cards')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='files')


class Comment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, related_name='users_comments')
    created_at = models.DateField(default=datetime.date.today)
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
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='mark_cards')
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, related_name='card_marks')


class FavouriteBoards(models.Model):
    user = models.ForeignKey(MyUser, related_name='users_faves', on_delete=models.SET_NULL, null=True)
    board = models.ForeignKey(Board, related_name='faves', on_delete=models.SET_NULL, null=True)