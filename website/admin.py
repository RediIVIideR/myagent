from django.contrib import admin
from .models import *
from ordered_model.admin import OrderedModelAdmin

# Register your models here.
admin.site.register(Slider)
admin.site.register(MainPageProperty)
# admin.site.register(Property)


class ItemAdmin(OrderedModelAdmin):
    list_display = ("property_name", "order", "move_up_down_links")


admin.site.register(Property, ItemAdmin)