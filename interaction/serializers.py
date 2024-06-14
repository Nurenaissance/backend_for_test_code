from rest_framework import serializers
from .models import Interaction
from custom_fields.models import CustomField


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = "__all__"

  

