from .models import Account
from .serializers import AccountSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer,CustomFieldSerializer
from custom_fields.models import CustomField
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from custom_fields.views import retrieve_custom_fields

class AccountListCreateAPIView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)
   
# @permission_classes([AllowAny])

class AccountDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)  
    
    def get(self, request, pk):
        account = Account.objects.get(pk=pk)
        serializer = AccountSerializer(account)

        # Access custom fields associated with the account
        custom_fields_data = []
        for custom_field in account.custom_fields.all():
            custom_fields_data.append({
                'custom_field': custom_field.custom_field,
                'value': custom_field.value,
                'field_type': custom_field.field_type
            })

        # Include custom fields in the response data
        data = {
            'account': serializer.data,
            'custom_fields': custom_fields_data
        }

        return Response(data)







