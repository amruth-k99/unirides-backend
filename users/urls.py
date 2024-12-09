from django.urls import path
from users.views import (
    create_user, delete_users, list_users
)

urlpatterns = [
    # params = [user_id]
    path("list/", list_users),
    path("create/", create_user),
    path("delete/", delete_users),
]
