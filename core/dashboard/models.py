from django.db import models

# Create your models here.

class Trade(models.Model):
    stock = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
    trade_type = models.CharField(max_length=10)  # Buy / Sell
    profit = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trade_type} - {self.stock}"