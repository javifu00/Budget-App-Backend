from unicodedata import category
from django.db import models
from django.dispatch import receiver
from djmoney.models.fields import MoneyField
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Func

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
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{} | {}: {}".format(self.author, self.receiver, self.amount)


class Goals(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    saved = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "{} | {}: {} / {}".format(
            self.author, self.title, self.saved, self.amount
        )


class Month(Func):
    function = "EXTRACT"
    template = "%(function)s(MONTH from %(expressions)s)"
    output_field = models.IntegerField()
