from rest_framework import serializers

from dashboard.models import Board, Issue, Label
from user.models import User


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'number']


class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name', 'color']


class IssueSerializer(serializers.ModelSerializer):
    assignee = AssigneeSerializer(read_only=True)
    labels = LabelSerializer(read_only=True, many=True)
    expiration_date = serializers.DateField(format='%d.%m.%Y')

    class Meta:
        model = Issue
        fields = ['id', 'name', 'number', 'assignee', 'labels', 'expiration_date']
