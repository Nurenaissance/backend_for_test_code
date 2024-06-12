from .models import Account
from .serializers import AccountSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer,CustomFieldSerializer
from custom_fields.models import CustomField

class AccountListCreateAPIView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)
   

class AccountDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)  # Allowing any user to access this view


@api_view(['GET'])
@permission_classes([AllowAny])
def get_account_with_custom_fields(request, model_name):
    accounts = Account.objects.all()  # Fetch all accounts

    if not model_name:
        return Response({'error': 'model_name is required'}, status=status.HTTP_400_BAD_REQUEST)

    custom_fields = CustomField.objects.filter(model_name=model_name, custom_field=accounts)
    serializer = CustomFieldSerializer(custom_fields, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)












     # def get_queryset(self):
    #     # Filter queryset based on user's tenant
    #     user_tenant = self.request.user.tenant
    #     return Account.objects.filter(tenant=user_tenant)

    # def perform_create(self, serializer):
    #     # Set the tenant of the account before saving
    #     serializer.save(tenant=self.request.user.tenant)

