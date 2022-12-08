from django.urls import path, include
from .user_auth.urls import urlpatterns as auth_staff
from .views import CardAPIListCreate, CardAPIView, ColumnAPIVListCreate, ColumnAPIView, BordAPIListCreate, BoardAPIView

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


] + auth_staff
