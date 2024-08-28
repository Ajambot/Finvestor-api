from django.db import models

# Create your models here.
from user_manager.models import User
class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=5)
    book_value = models.FloatField()
    amount = models.FloatField()