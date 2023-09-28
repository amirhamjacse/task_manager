from django.contrib import admin
from tasks import models

# Register your models here.


@admin.register(models.CustomUser)
class UserModelAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'username',
        'date_joined',
        'is_active',
        'is_staff',
    ]
    # list_editable = [
    #     "order"
    # ]
    # search_fields = ['name', 'type', 'wing_or_zone', "circle"]
    # readonly_fields = ('created_at', 'last_updated')
    # list_filter = ['is_active']
    # ordering = ("order", "-pk")
