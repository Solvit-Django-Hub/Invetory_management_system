from django.urls import path
from .views import  ProfileView, LogoutView, UserListView, CreateUserView

urlpatterns = [
    
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/create/", CreateUserView.as_view(), name="user-create"),
]