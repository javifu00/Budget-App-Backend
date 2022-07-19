from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
