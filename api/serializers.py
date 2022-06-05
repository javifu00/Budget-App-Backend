from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Goals, Transaction


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class GoalSerializer(ModelSerializer):
    class Meta:
        model = Goals
        fields = "__all__"
