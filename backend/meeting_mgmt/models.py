from django.db import models
from django.contrib.auth import get_user_model

class Meeting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    meeting_time = models.DateTimeField()
    organizer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    attendees = models.ManyToManyField(get_user_model(), related_name='meetings_attending')
    google_meet_link = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.title)
