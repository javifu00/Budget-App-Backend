from django.urls import path
from . import views

urlpatterns = [
    path("", views.getGoals, name="goals"),
    path("<str:pk>", views.getGoal, name="goal"),
    path("create/", views.createGoal, name="create-goal"),
    path("<str:pk>/delete/", views.deleteGoal, name="delete-goal"),
    path("<str:pk>/update/", views.updateGoal, name="update-goal"),
    # path("", views.getGoals, name="profile"),
]
