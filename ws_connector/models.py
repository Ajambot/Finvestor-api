from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Position(models.Model):
    account_id = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=5)
    book_value = models.FloatField()
    amount = models.FloatField()

class Credential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ws_access_token = models.CharField(max_length=255, blank=True)
    ws_refresh_token = models.CharField(max_length=255, blank=True)
    ws_access_token_expiry = models.DateTimeField(blank=True, null=True)
