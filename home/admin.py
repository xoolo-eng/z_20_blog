from django.contrib import admin
from home.models import FeedBack


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ("email", "active")


admin.site.register(FeedBack, FeedBackAdmin)
