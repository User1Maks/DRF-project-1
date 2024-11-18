from django.contrib import admin

from users.models import User, Subscriptions

admin.site.register(User)


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'course',)
    list_filter = ('user', 'course',)
    search_fields = ('user', 'course',)

