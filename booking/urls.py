from django.urls import path
from .views import BookRoom


urlpatterns = [
    path("", BookRoom.as_view(), name='book-room')
]
