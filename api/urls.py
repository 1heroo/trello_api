from django.urls import path
from .user_auth.urls import urlpatterns as auth_urls
from .views import CardAPIListCreate, CardAPIView, ColumnAPIVListCreate, ColumnAPIView, BordAPIListCreate, BoardAPIView, \
    CommentAPIView, MarkAPIListCreate, MarkAPIView



urlpatterns = [
    # card crud
    path('card/create-list/', CardAPIListCreate.as_view(), name='card-list-api'),
    path('card/<int:pk>/', CardAPIView.as_view(), name='card-api'),

    # column crud
    path('column/create-list/',  ColumnAPIVListCreate.as_view(), name='column-list-api'),
    path('column/<int:pk>',  ColumnAPIView.as_view(), name='column-api'),

    # board crud
    path('board/create-list/', BordAPIListCreate.as_view(), name='board-list-api'),
    path('board/<int:pk>', BoardAPIView.as_view(), name='board-api'),

    # mark crud
    path('mark/', MarkAPIListCreate.as_view(), name='mark-list-api'),
    path('mark/<int:pk>', MarkAPIView.as_view(), name='mark-api'),

    path('comment/create/', CommentAPIView.as_view(), name='create-comment')


    # login staff

    # path('logic/')
] + auth_urls
