from datetime import date, datetime
from decimal import Decimal
from enum import auto
from multiprocessing import context
from sqlite3 import Date
from django.dispatch import receiver
from django.shortcuts import render
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.cache import never_cache
from rest_framework.permissions import IsAuthenticated
from .models import Month, Transaction, Goals
from .serializers import TransactionSerializer, GoalSerializer
from django.db import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models.functions import TruncMonth

# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        {
            "Endpoint": "/transactions",
            "method": "GET",
            "body": None,
            "description": "Returns an array of notes",
        },
        {
            "Endpoint": "/transactions/id",
            "method": "GET",
            "body": None,
            "description": "Returns a single note object",
        },
        {
            "Endpoint": "/transactions/create/",
            "method": "POST",
            "body": {"body": ""},
            "description": "Creates new note with data sent in post request",
        },
        {
            "Endpoint": "/transactions/id/update/",
            "method": "PUT",
            "body": {"body": ""},
            "description": "Creates an existing note with data sent in post request",
        },
        {
            "Endpoint": "/transactions/id/delete/",
            "method": "DELETE",
            "body": None,
            "description": "Deletes an exiting transaction",
        },
        {
            "Endpoint": "/goals/",
            "method": "GET",
            "body": None,
            "description": "Returns an array of goals",
        },
        {
            "Endpoint": "/goals/id",
            "method": "GET",
            "body": None,
            "description": "Returns a single goal object",
        },
        {
            "Endpoint": "/goals/create/",
            "method": "POST",
            "body": {"body": ""},
            "description": "Creates new goal with data sent in post request",
        },
        {
            "Endpoint": "/goals/id/update/",
            "method": "PUT",
            "body": {"body": ""},
            "description": "Edits an existing goal with data sent in post request",
        },
        {
            "Endpoint": "/goals/id/delete/",
            "method": "DELETE",
            "body": None,
            "description": "Deletes and exiting goal",
        },
    ]
    return Response(routes)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTransactions(request):
    user = request.user
    transactions = user.transaction_set.all().order_by("-date")
    transactionByMonths = (
        user.transaction_set.annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total_sum_months=Sum("amount"))
    )
    transactionsIn = transactions.filter(transaction_way="I").aggregate(Sum("amount"))
    transactionsOut = transactions.filter(transaction_way="O").aggregate(Sum("amount"))
    transactionsByCategory = (
        user.transaction_set.values("category", "transaction_way")
        .annotate(total_expenses=Sum("amount"))
        .order_by("-total_expenses")
    )
    categoryNames = []
    categoryAmount = []
    expensesByMonths = {
        "totalSpent": [],
        "months": [],
    }
    for row in transactions:
        print(row)
    print("\n")
    for category in transactionsByCategory:
        print(category)
        if category["transaction_way"] == "O" and category["category"] != "goal":
            categoryNames.append(category["category"])
            categoryAmount.append(category["total_expenses"])

    for monthlySpent in transactionByMonths:
        print(monthlySpent["month"])
        expensesByMonths["totalSpent"].append(monthlySpent["total_sum_months"])
        expensesByMonths["months"].append(monthlySpent["month"])

    balance = transactionsIn["amount__sum"] - transactionsOut["amount__sum"]
    serializer = TransactionSerializer(transactions, many=True)
    dataDict = {
        "serializer": serializer.data,
        "balance": balance,
        "expenses": transactionsOut["amount__sum"],
        "income": transactionsIn["amount__sum"],
        "categoryNames": categoryNames,
        "categoryAmount": categoryAmount,
        "expensesByMonth": expensesByMonths["totalSpent"],
        "expensesMonths": expensesByMonths["months"],
    }

    return Response(dataDict)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createTransaction(request):
    data = request.data
    user = request.user

    transaction = Transaction.objects.create(
        amount=data["amount"],
        author=user,
        category=data["category"],
        date=data["date"],
        receiver=data["receiver"],
        transaction_way=data["transaction_way"],
    )
    serializer = TransactionSerializer(transaction, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def getTransactionsBalance(request):
    transactionsIn = Transaction.objects.aggregate(sum("amount")).get(
        transaction_way="I"
    )
    transactionsOut = Transaction.objects.aggregate(sum("amount")).get(
        transaction_way="I"
    )
    # serializer = TransactionSerializer(transactions, many=True)
    return  # Response(serializer.data)


@api_view(["GET"])
def getTransaction(request, pk):
    transactions = Transaction.objects.get(id=pk)
    serializer = TransactionSerializer(transactions)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteTransaction(request, pk):
    transaction = Transaction.objects.get(id=pk)
    transaction.delete()
    return Response("Transaction was deleted!")


@api_view(["GET"])
def getGoals(request):
    goals = Goals.objects.all()
    serializer = GoalSerializer(goals, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getGoal(request, pk):
    goals = Goals.objects.get(id=pk)
    serializer = GoalSerializer(goals)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createGoal(request):
    data = request.data
    user = request.user
    goal = Goals.objects.create(
        title=data["title"],
        amount=data["amount"],
        saved=data["saved"],
        author=user,
    )
    serializer = GoalSerializer(goal, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteGoal(request, pk):
    goal = Goals.objects.get(id=pk)
    goal.delete()
    return Response("Goal was deleted!")


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateGoal(request, pk):
    data = request.data
    data["author"] = request.user.id
    goal = Goals.objects.get(id=pk)
    print(data)
    serializer = GoalSerializer(goal, data=data)

    if serializer.is_valid():
        serializer.save()
    print(serializer.errors)
    return Response(serializer.data)
