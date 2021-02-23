from django.db import models


class Log(models.Model):
    path = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    execution_time_sec = models.DecimalField(max_digits=8, decimal_places=4)

    def __str__(self):
        return f'{self.path} {self.execution_time_sec}'
