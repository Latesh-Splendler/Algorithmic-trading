from django.contrib import admin

from .models import (
    Stock,

    PriceData,
    Momentum,
    TradingSignal,
    RebalanceEvent,
)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'ticker',
        'name',
        'sector',
        'is_active',
        'created_at',
    )

    list_filter = (
        'is_active',
        'sector',
    )

    search_fields = (
        'ticker',
        'name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )





@admin.register(PriceData)
class PriceDataAdmin(admin.ModelAdmin):
    list_display = (
        'stock',
        'date',
        'close_price',
        'volume',
    )

    list_filter = (
        'date',
        'stock',
    )

    search_fields = (
        'stock__ticker',
    )

    readonly_fields = (
        'created_at',
    )

    date_hierarchy = 'date'


@admin.register(Momentum)
class MomentumAdmin(admin.ModelAdmin):
    list_display = (
        'stock',
        'date',
        'momentum_score',
        'rank',
        'quintile',
        'is_top_quintile',
    )

    list_filter = (
        'date',
        'quintile',
        'is_top_quintile',
    )

    search_fields = (
        'stock__ticker',
    )

    readonly_fields = (
        'created_at',
    )

    date_hierarchy = 'date'


@admin.register(TradingSignal)
class TradingSignalAdmin(admin.ModelAdmin):
    list_display = (
        'stock',
        'signal_date',
        'signal_type',
        'momentum',
    )

    list_filter = (
        'signal_type',
        'signal_date',
    )

    search_fields = (
        'stock__ticker',
    )

    date_hierarchy = 'signal_date'


@admin.register(RebalanceEvent)
class RebalanceEventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
    )