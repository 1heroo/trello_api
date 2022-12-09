from django.urls import path
from .user_auth.urls import urlpatterns as auth_urls
from .CRUD.urls import urlpatterns as crud_urls
from .views import InviteMemberToBoardView, InviteToCard, AddToFaves, ArchivingView

urlpatterns = [
    path('logic/invite-member-to-board/', InviteMemberToBoardView.as_view(), name='invite-member-to-board'),
    path('logic/invite-member-to-card/', InviteToCard.as_view(), name='invite-member-to-card'),

    path('logic/faves', AddToFaves.as_view(), name='add-to-faves'),
    path('logic/archive-unarchive/', ArchivingView.as_view(), name='archiving')
] + auth_urls + crud_urls
