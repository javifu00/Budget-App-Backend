from django.urls import path, include
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
    path("transactions/", include("transaction.urls")),
    # Goals URL's
    path("goals/", include("goals.urls")),
    # Stadistics URL's
    path("stadistics/", include("goals.urls")),
    # Profile URL's
    path("profile/", include("goals.urls")),
]
