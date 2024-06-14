from rest_framework import serializers
from .models import CustomField,Account


class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = "__all__"

class AccountSerializer(serializers.ModelSerializer):
    custom_fields = serializers.SerializerMethodField()
    
    class Meta:
        model = Account
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        custom_fields = data.pop('custom_fields', None)
        if custom_fields is not None:
            data['custom_fields'] = custom_fields

        return data

    
    def get_custom_fields(self, obj):
        model_name = 'account' 
        account_id = obj.id  

        custom_fields = CustomField.objects.filter(model_name=model_name)

        custom_fields_data = []
        for field in custom_fields:
            if field.entity_id == account_id:
                value = field.value
            else:
                value = None

            custom_fields_data.append({
                'custom_field': field.custom_field,
                'value': value,
                'field_type': field.field_type
            })

        return custom_fields_data