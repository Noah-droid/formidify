import uuid
from django.db import models

class Form(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    data = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Form {self.unique_id} submitted at {self.created_at}"