import imp
from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path("", views.getRoutes, name="routes"),
    # Token URL's
    path("token/", MyTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    # Transactions  URL's
    path("transactions/", views.getTransactions, name="transactions"),
    path("transactions/<str:pk>", views.getTransaction, name="transaction"),
    path("transactions/create/", views.createTransaction, name="create-transaction"),
    path(
        "transactions/<str:pk>/delete/",
        views.deleteTransaction,
        name="delete-transaction",
    ),
    # Goals URL's
    path("goals/", views.getGoals, name="goals"),
    path("goals/<str:pk>", views.getGoal, name="goal"),
    path("goals/create/", views.createGoal, name="create-goal"),
    path("goals/<str:pk>/delete/", views.deleteGoal, name="delete-goal"),
    path("goals/<str:pk>/update/", views.updateGoal, name="update-goal"),
    path("stadistics/", views.getGoals, name="stadistics"),
    path("profile/", views.getGoals, name="profile"),
]
