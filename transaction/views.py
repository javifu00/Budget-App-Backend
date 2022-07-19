from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from transaction.services import getDataTransactions
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTransactions(request):
    transactionsDict = getDataTransactions(request, None)
    return Response(transactionsDict)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTransactionsHome(request):
    transactionsDict = getDataTransactions(request, 10)
    return Response(transactionsDict)


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
