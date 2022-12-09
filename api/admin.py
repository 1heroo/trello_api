from .models import (MyUser, Comment, Card, Column,
                     Board, Mark, Members,
                     MarkCard, BoardMembers, FavourBoards)
from django.contrib import admin


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email', )
    list_display_links = ('pk', 'first_name', 'last_name', 'email',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_display_links = ('pk', 'title')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_display_links = ('pk', 'title')


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_display_links = ('pk', 'title')


class MarkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_display_links = ('pk', 'title')


# models
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Comment)
admin.site.register(Card, ItemAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Mark, MarkAdmin)
admin.site.register(FavourBoards)

# relations
admin.site.register(Members)
admin.site.register(MarkCard)
admin.site.register(BoardMembers)
