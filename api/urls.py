from django.urls import path
from .user_auth.urls import urlpatterns as auth_urls
from .CRUD.urls import urlpatterns as crud_urls


urlpatterns = [

] + auth_urls + crud_urls
