from django.urls import path, include
from .user_auth.urls import urlpatterns as auth_staff
from .views import CardAPIListCreate, CardAPIView

urlpatterns = [
    path('card/', CardAPIListCreate.as_view(), name='item-list-api'),
    path('card/<int:pk>/', CardAPIView.as_view(), name='item-api'),

] + auth_staff