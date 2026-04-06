from rest_framework import serializers
from .models import Game


# DynamicFieldsModelSerializer
# https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class GameSerializer(DynamicFieldsModelSerializer):
    """Serializer para el modelo Game, con un campo adicional para representar el tablero como una matriz 3x3."""
    player1_name = serializers.CharField(source="player1.name", read_only=True)
    player2_name = serializers.CharField(source="player2.name", read_only=True)
    current_turn_name = serializers.CharField(source="current_turn.name", read_only=True)

    board_matrix = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            "id",
            "player1_name",
            "player2_name",
            "board_state",
            "current_turn_name",
            "status",
            "winner",
            "moves",
            "board_matrix",
        ]
        read_only_fields = [
            "current_turn_name",
            "status",
            "winner",
            "moves",
            "board_state",
        ]

    def get_board_matrix(self, obj):
        """Convierte el estado del tablero (cadena de 9 caracteres)
        en una matriz 3x3 para facilitar su representación en la API."""
        return [list(obj.board_state[i : i + 3]) for i in range(0, 9, 3)]
