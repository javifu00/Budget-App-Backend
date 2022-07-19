from django.db import models
from djmoney.models.fields import MoneyField
from django.db.models import Func
from django.conf import settings

# Create your models here.


class Transaction(models.Model):
    TRANSACTION_WAYS = (
        ("I", "In"),
        ("O", "Out"),
    )
    receiver = models.CharField(max_length=100)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    transaction_way = models.CharField(max_length=3, choices=TRANSACTION_WAYS)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{} | {}: {}".format(self.author, self.receiver, self.amount)


class Month(Func):
    function = "EXTRACT"
    template = "%(function)s(MONTH from %(expressions)s)"
    output_field = models.IntegerField()
