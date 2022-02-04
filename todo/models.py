from datetime import datetime
from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
User = get_user_model()


class Task(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  title = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  complete = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)
  
  def __str__(self) -> str:
      return self.title
  def get_absolute_url(self):
      return reverse("task-detail", kwargs={"pk": self.pk})
  
  class Meta:
    ordering = ['complete']