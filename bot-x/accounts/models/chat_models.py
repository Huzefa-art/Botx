

# class ChatLogs(models.Model):
#     message_type = models.CharField(max_length=10)
#     message_text = models.TextField()
#     message_audio = models.URLField()
#     is_user = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         managed = False  # Ensure Django doesn't try to manage migrations for this model
#         _use_db = 'mongo'
#         ordering = ('-created_at',)

#     def __str__(self):
#        return self.message_text