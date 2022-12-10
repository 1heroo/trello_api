from django.urls import path, re_path
from .user_auth.urls import urlpatterns as auth_urls
from .CRUD.urls import urlpatterns as crud_urls
from .views import InviteMemberToBoardView, AddToMemberCard, FavouriteBoardsAPIView, ArchivingView, SearchView


urlpatterns = [
    path('logic/invite-member-to-board/', InviteMemberToBoardView.as_view(), name='invite-member-to-board'),
    path('logic/invite-member-to-card/', AddToMemberCard.as_view(), name='invite-member-to-card'),

    path('logic/favourite-boards', FavouriteBoardsAPIView.as_view(), name='favourite_boards'),
    path('logic/archive-unarchive/', ArchivingView.as_view(), name='archiving'),

    re_path('^filtering/(?P<query>.+)/$', SearchView.as_view(), name='search')
] + auth_urls + crud_urls
