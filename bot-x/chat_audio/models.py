from django.db import models

class AudioFile(models.Model):
    # audio = models.FileField(upload_to='audio_files/')
     audio = models.FileField(upload_to='audio/',default='default_filename.mp3')
