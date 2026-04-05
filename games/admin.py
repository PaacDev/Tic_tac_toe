from django.contrib import admin

from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "player1", "player2", "status")
    list_filter = ("status",)
    search_fields = ("player1__name", "player2__name")
