# leads/serializers.py

from rest_framework import serializers
from .models import Lead
from custom_fields.models import CustomField

class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = '__all__'

class LeadSerializer(serializers.ModelSerializer):
    custom_fields = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)


        custom_fields = data.pop('custom_fields', None)
        if custom_fields is not None:
            data['custom_fields'] = custom_fields

        return data

    def get_custom_fields(self, obj):
        model_name = 'lead' 
        lead_id = obj.id  
        custom_fields = CustomField.objects.filter(model_name=model_name)

        # Prepare custom fields data
        custom_fields_data = []
        for field in custom_fields:
            if field.entity_id == lead_id:
                value = field.value
            else:
                value = None

            custom_fields_data.append({
                'custom_field': field.custom_field,
                'value': value,
                'field_type': field.field_type
            })

        return custom_fields_data
