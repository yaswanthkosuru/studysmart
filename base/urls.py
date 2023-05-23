from django.urls import path
from .views import (
    home,
    room,
    create_room,
    update_room,
    delete_room,
    loginpage,
    logoutUser,
    registeruser,
    delete_message,
)

urlpatterns = [
    path("login/", loginpage, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("register/", registeruser, name="register"),
    path("", home, name="home"),
    path("room/<str:pk>/", room, name="room"),
    path("create_room/", create_room, name="create_room"),
    path("update_room/<str:pk>/", update_room, name="update_room"),
    path("delete_room/<str:pk>/", delete_room, name="delete_room"),
    path("delete_message/<str:pk>/", delete_message, name="delete_message"),
]
