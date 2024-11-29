from rest_framework import serializers
from .models import Objective, KeyResult, Task

class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = '__all__'

class KeyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyResult
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

