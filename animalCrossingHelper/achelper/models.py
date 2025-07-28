from django.db import models

class Item(models.Model):
    row = models.IntegerField()
    column = models.IntegerField()
    name = models.CharField(max_length=100)
    shadow_size = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    hemisphere = models.CharField(max_length=100)
    months = models.CharField(max_length=100)
    always_available = models.BooleanField(default=False)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return f"Item ({self.row}, {self.column})"