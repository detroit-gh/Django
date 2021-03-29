from bulk_update_or_create import BulkUpdateOrCreateQuerySet

from django.db import models
from django.utils import timezone


class ExchangeRate(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    currency_id = models.CharField(max_length=6, primary_key=True)
    currency = models.CharField(max_length=3)
    buy = models.DecimalField(max_digits=8, decimal_places=3)
    buy_change = models.IntegerField(default=0)
    sell = models.DecimalField(max_digits=8, decimal_places=3)
    sell_change = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)

    def to_dict(self):
        return {
            f"{self.currency}_buy": self.buy,
            f"{self.currency}_buy_change": check_stat(self.buy_change),
            f"{self.currency}_sell": self.sell,
            f"{self.currency}_sell_change": check_stat(self.sell_change),
        }


def check_stat(status):
    if status == 1:
        return "lightgreen"
    elif status == -1:
        return "lightcoral"
    else:
        return "white"
