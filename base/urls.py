from django.urls import path
from . import views

urlpatterns=[
    path('login/', views.log, name="login"),
    path('logout/', views.logou, name="logout"),
    path('register/', views.rega, name="register"),

    path('', views.home, name="home"),
    path('room/<str:ids>/', views.room, name="room"),
    path('profile/<str:ids>', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:ids>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:ids>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:ids>/', views.deleteMessage, name="delete-message")
]