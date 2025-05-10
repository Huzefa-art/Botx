from django.db import models
from django.conf import settings
from accounts.models.user_models import User
import os
from datetime import datetime

def upload_to(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    new_filename = f'{instance.user_id}/{base_filename}_{timestamp}{file_extension}'
    return os.path.join('profile_clone_audio/', new_filename)

class Profile(models.Model):
    """Profiles of User's Friendlist."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    conversation = models.TextField(default='My conversation')
    audiofilename = models.FileField(upload_to=upload_to,default='default_filename.mp3')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'accounts'


# from django.db import models
# class Profile(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     role = models.CharField(max_length=50)
#     conversation = models.TextField()
#     audio_file = models.FileField(upload_to ='uploads/')
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return self.name
