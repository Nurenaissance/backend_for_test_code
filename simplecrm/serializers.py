from rest_framework import serializers

class AddEntitySerializer(serializers.Serializer):
    tenant_id = serializers.IntegerField()
    model_name = serializers.CharField()
    entity_data = serializers.ListField(child=serializers.DictField())

    def validate_model_name(self, value):
        # Add custom validation for model_name if needed
        # For example, check if the model_name corresponds to a predefined model
        if value not in ['Account', 'Contact']:  # Update with your predefined models
            raise serializers.ValidationError("Invalid model name")
        return value