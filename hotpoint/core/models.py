from django.db import models

class Voucher(models.Model):
    code = models.CharField(max_length=20, unique=True)
    duration_minutes = models.IntegerField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.duration_minutes} min - {'Used' if self.used else 'Unused'}"
    
class PricingPlan(models.Model):
    amount = models.PositiveIntegerField(unique=True, help_text="Amount in KES (e.g., 10, 20, 50)")
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes (e.g., 30, 60, 180)")

    def __str__(self):
        return f"{self.amount} KES = {self.duration_minutes} minutes"

