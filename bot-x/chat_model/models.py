from django.db import models
from django.conf import settings
from accounts.models.user_models import User
from accounts.models.profile_models import Profile

class chat_model(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=50)
    chat = models.TextField(default='My conversation')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "chat_history"
        app_label = 'chat_model'



