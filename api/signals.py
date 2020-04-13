from .models import Wallet, Operation
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# @receiver(post_save, sender=Operation)
# def update_wallet_balance(sender, instance, **kwargs):
