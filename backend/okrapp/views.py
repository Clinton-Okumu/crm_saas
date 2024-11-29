from rest_framework import viewsets
from .models import Objective, KeyResult, Task
from .serializers import ObjectiveSerializer, KeyResultSerializer, TaskSerializer
from .permissions import IsSuperAdmin, IsProjectAdmin, IsHRManager, IsOwnerOrReadOnly

class ObjectiveViewSet(viewsets.ModelViewSet):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer
    permission_classes = [IsSuperAdmin | IsProjectAdmin | IsHRManager | IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign the current user as the owner of the objective
        serializer.save(owner=self.request.user)

class KeyResultViewSet(viewsets.ModelViewSet):
    queryset = KeyResult.objects.all()
    serializer_class = KeyResultSerializer
    permission_classes = [IsSuperAdmin | IsProjectAdmin | IsHRManager | IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign the objective owner to key results as well
        objective = serializer.validated_data.get('objective')
        if objective:
            serializer.save(owner=objective.owner)  # Ensure the key result inherits the objective's owner

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsSuperAdmin | IsProjectAdmin | IsHRManager | IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign the key result owner to tasks as well
        key_result = serializer.validated_data.get('key_result')
        if key_result:
            serializer.save(owner=key_result.objective.owner)  # Ensure the task inherits from the objective owner

