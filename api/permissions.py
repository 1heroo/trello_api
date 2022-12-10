from rest_framework import permissions


class BoardOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated \
            | (request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsMemberOrBoardOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (user in obj.members.all()) \
               | (user == obj.column.board.author)
