from django.db import models
from users.models import CustomUser

class Objective(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="objectives")
    due_date = models.DateField()

    def __str__(self):
        return self.title

class KeyResult(models.Model):
    objective = models.ForeignKey(Objective, related_name="key_results",null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    target_value = models.FloatField()
    current_value = models.FloatField()

    def __str__(self):
        return f"{self.title} ({self.objective.title})"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

