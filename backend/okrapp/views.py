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
        serializer.save()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsSuperAdmin | IsProjectAdmin | IsHRManager | IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()
