from django.contrib import admin
from .models import Product, Neighborhood, SimulationDay, Door, DoorInteractionLog


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'commission_per_sale', 'commission_per_appointment')


@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_type', 'economic_level', 'door_count', 'open_rate')


@admin.register(SimulationDay)
class SimulationDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'neighborhood', 'product', 'doors_knocked', 'sales_closed', 'is_completed', 'created_at')


@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    list_display = ('door_number', 'simulation_day', 'resident_name', 'archetype', 'status', 'interest', 'patience')
    list_filter = ('status', 'archetype')


@admin.register(DoorInteractionLog)
class DoorInteractionLogAdmin(admin.ModelAdmin):
    list_display = ('door', 'turn_index', 'tactic_type', 'interest_change', 'patience_change')
