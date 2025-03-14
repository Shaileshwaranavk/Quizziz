from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    username = models.CharField(max_length=100, unique=True)  # Ensure unique username
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)  # Ensure unique email
    password = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Question(models.Model):
    text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)

    def __str__(self):
        return self.text