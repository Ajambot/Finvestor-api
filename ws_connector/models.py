from django.db import models

# Create your models here.
class Position(models.Model):
    symbol = models.CharField(max_length=5)
    book_value = models.FloatField()
    amount = models.FloatField()