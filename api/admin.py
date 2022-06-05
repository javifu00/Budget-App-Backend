from django.contrib import admin

# Register your models here.

from .models import Transaction
from .models import Goals

admin.site.register(Transaction)
admin.site.register(Goals)
