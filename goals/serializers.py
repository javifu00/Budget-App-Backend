from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Goals
from transaction.models import Transaction


class GoalSerializer(ModelSerializer):
    class Meta:
        model = Goals
        fields = "__all__"
