from django.contrib import admin
from .models import Wallet, Operation


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'balance', 'created')


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'wallet', 'type', 'amount')
    list_filter = ('wallet', 'type', 'date')
    search_fields = ('wallet',)
