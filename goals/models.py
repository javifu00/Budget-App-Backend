from django.db import models
from djmoney.models.fields import MoneyField
from django.conf import settings
from django.db.models import Func

# Create your models here.


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
