from django.db import models

# Create your models here.
class Index(models.Model):
    name = models.CharField(max_length=255)
    # created_at = models.DateTimeField(default=models.DateTimeField(auto_now_add=True))


class DailyPrice(models.Model):
    index = models.ForeignKey(Index, on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    shares_traded = models.PositiveIntegerField()
    turnover = models.DecimalField(max_digits=15, decimal_places=2)
    # created_at = models.DateTimeField(default=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return (self.index.name)