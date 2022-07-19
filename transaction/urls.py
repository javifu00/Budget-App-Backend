from django.urls import path
from . import views


urlpatterns = [
    # Transactions  URL's
    path("", views.getTransactions, name="transactions"),
    path("home/", views.getTransactionsHome, name="transactions"),
    path("<str:pk>", views.getTransaction, name="transaction"),
    path("create/", views.createTransaction, name="create-transaction"),
    path(
        "<str:pk>/delete/",
        views.deleteTransaction,
        name="delete-transaction",
    ),
]
