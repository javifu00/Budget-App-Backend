from django.db.models import Sum
from .serializers import TransactionSerializer
from django.db.models.functions import TruncMonth


def getDataTransactions(request, limit):
    user = request.user
    transactionsSet = user.transaction_set.all().order_by("-date")
    if len(transactionsSet) == 0:
        return {0}
    categoryNames, categoryAmount = getTransactionByCategory(transactionsSet)
    serializer = TransactionSerializer(transactionsSet, many=True)
    transactionsList = serializer.data
    if limit is not None:
        print("\n\n")
        print(transactionsList[:2])
        transactionsList = transactionsList[:10]
    balance, transactionsIn, transactionsOut = getBalance(transactionsSet)
    expensesByMonths = getTransactionByMonth(transactionsSet)
    dataDict = {
        "serializer": transactionsList,
        "balance": balance,
        "expenses": transactionsOut["amount__sum"],
        "income": transactionsIn["amount__sum"],
        "categoryNames": categoryNames,
        "categoryAmount": categoryAmount,
        "expensesByMonth": expensesByMonths["totalSpent"],
        "expensesMonths": expensesByMonths["months"],
    }
    return dataDict


def getBalance(transactionsSet):
    transactionsIn = transactionsSet.filter(transaction_way="I").aggregate(
        Sum("amount")
    )

    transactionsOut = transactionsSet.filter(transaction_way="O").aggregate(
        Sum("amount")
    )
    if transactionsIn["amount__sum"] == None:
        transactionsIn["amount__sum"] = 0.00
    if transactionsOut["amount__sum"] == None:
        transactionsOut["amount__sum"] = 0
    return (
        transactionsIn["amount__sum"] - transactionsOut["amount__sum"],
        transactionsIn,
        transactionsOut,
    )


def getTransactionByMonth(transactionsSet):
    transactionByMonths = (
        transactionsSet.annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total_sum_months=Sum("amount"))
    )
    expensesByMonths = {
        "totalSpent": [],
        "months": [],
    }

    for index, monthlySpent in enumerate(transactionByMonths):
        if index >= 6:
            break
        expensesByMonths["totalSpent"].insert(0, monthlySpent["total_sum_months"])
        expensesByMonths["months"].insert(0, monthlySpent["month"])

    return expensesByMonths


def getTransactionByCategory(transactionsSet):
    transactionsByCategory = (
        transactionsSet.values("category", "transaction_way")
        .annotate(total_expenses=Sum("amount"))
        .order_by("-total_expenses")
    )
    categoryNames = []
    categoryAmount = []
    for category in transactionsByCategory:
        if category["transaction_way"] == "O" and category["category"] != "goal":
            categoryNames.append(category["category"])
            categoryAmount.append(category["total_expenses"])
    return categoryNames, categoryAmount
