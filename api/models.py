from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class Wallet(models.Model):
    name = models.CharField(max_length=250, blank=False, unique=True)
    balance = models.DecimalField(blank=False, decimal_places=2, max_digits=12)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created', 'name']

    def __str__(self):
        return f"{self.name}"


class Operation(models.Model):
    OPERATION_TYPE = ((0, "Costs"),
                      (1, "Income"))

    date = models.DateTimeField(blank=False, default=timezone.now)
    type = models.IntegerField(choices=OPERATION_TYPE, blank=False)
    amount = models.DecimalField(blank=False, decimal_places=2, max_digits=12,
                                 validators=[
                                     MinValueValidator(Decimal('0.01'))])
    comment = models.CharField(max_length=250, blank=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE,
                               related_name="operations")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{['Расход', 'Доход'][self.type]}: {self.amount} руб."

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Operation, self).save(*args, **kwargs)
        if created:
            self._update_wallet(created)

    def delete(self, using=None, keep_parents=False):
        self._update_wallet()
        super(Operation, self).delete()

    def _update_wallet(self, save=False):
        if save:
            sum = self.amount if self.type == 1 else -self.amount
        else:
            sum = self.amount if self.type == 0 else -self.amount

        self.wallet.balance += sum
        self.wallet.save()
