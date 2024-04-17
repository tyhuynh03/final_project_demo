from django.db import models
from users.models import User
from django.conf import settings
class Topic(models.Model):
    name = models.CharField(max_length=255)
    User = settings.AUTH_USER_MODEL
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=3)
    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.CharField(max_length=255)
    default_topic_id = 1  # ID của chủ đề mặc định đã tồn tại trong cơ sở dữ liệu
    topic = models.ForeignKey(Topic, related_name='questions', on_delete=models.CASCADE, default=default_topic_id)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
