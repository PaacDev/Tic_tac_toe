from rest_framework import serializers

from .models import Player


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ["name"]

    def create(self, validated_data):
        user = self.context["request"].user
        player = Player.objects.create(user=user, **validated_data)
        return player
