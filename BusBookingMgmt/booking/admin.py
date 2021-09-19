from django.contrib import admin
from booking.models import (VehicalDetail,
                            DriverDetail, BusService, BusTiming,
                            Query)


@admin.register(VehicalDetail)
class VehicalDetailAdmin(admin.ModelAdmin):
    list_display = ("vehicle_name", "vehicle_registration_number",
                    "engine_number", "mfg_date", "number_of_seats",
                    "fuel_capacity", "owner_name", "ac", "non_ac")
    search_fields = ("vehicle_registration_number", "engine_number")


@admin.register(DriverDetail)
class DriverDetailAdmin(admin.ModelAdmin):
    list_display = ("driver_name", "driver_email", "driver_phone_no",
                    "driver_adress", "driver_licence")

    search_fields = ("driver_email", "driver_phone_no", "driver_licence")


class BusTimingAdmin(admin.TabularInline):
    model = BusTiming
    extra = 0
    fk_name = 'service'


@admin.register(BusService)
class BusServiceAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "source", "destination",
                    "souce_bus_stand_location", "destination_bus_stand_location",
                    "passanger_capacity", "per_passanger_price", "driver_email",
                    "created_date", "modified_date")

    inlines = [BusTimingAdmin, ]

    raw_id_fields = ('driver_email',)


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):

    list_display = ("attrs", "created_date", "modified_date")
    search_fields = ("id",)
