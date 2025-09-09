from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ChatBotMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=200)
    if_bot = models.BooleanField(default=False)
    def __str__(self):
        if self.if_bot == True:     
            return self.user.email + self.timestamp.isoformat() + "-bot"
        else:
            return self.user.email + self.timestamp.isoformat() + "-user"
    