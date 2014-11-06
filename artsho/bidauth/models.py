from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):
    user = models.ForeignKey(User)
    token = models.TextField(blank=False, db_index=True)
