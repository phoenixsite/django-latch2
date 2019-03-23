from django.contrib import admin
from latch.models import LatchSetup


class LatchSetupAdmin(admin.ModelAdmin):
    list_display = ("latch_appid", "latch_secret")

    def has_add_permission(self, request):
        return not LatchSetup.objects.exists()


admin.site.register(LatchSetup, LatchSetupAdmin)
