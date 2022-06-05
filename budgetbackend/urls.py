from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# path("", include("base.urls"))
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls")),
]
