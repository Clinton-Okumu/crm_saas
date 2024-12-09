# okrapp/serializers.py
from rest_framework import serializers
from .models import Objective, KeyResult, Task

class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = '__all__'

class KeyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyResult
        fields = ['objective', 'title', 'target_value', 'current_value']
        extra_kwargs = {
            'objective': {'required': False, 'allow_null': True}
        }

    def validate_objective(self, value):
        # Ensure the objective exists if it's provided
        if value and not Objective.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Objective with this ID does not exist.")
        return value

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

