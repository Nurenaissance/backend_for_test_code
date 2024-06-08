# views.py
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from twilio.twiml.messaging_response import MessagingResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models, connection
from django.apps import apps
from .models import Tenant
from .serializers import AddEntitySerializer

def get_result_from_query(query: str, zipName: str, prompt: str) -> str:
    url = 'https://59a8-14-142-75-54.ngrok-free.app/api/get-pdf/'
    headers = {'Content-Type': 'application/json'}

    data = {
        'message': query,
        'zipName': zipName,
        'prompt': prompt,
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        return response_data.get('answer', '')
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return ''


@csrf_exempt
def incoming_sms(request):
    if request.method == 'POST':
        # Get the message the user sent to our Twilio number
        body = request.POST.get('Body', None)
        
        print(f"Received message: {body}")  # Add this print statement to check the received message

        # Start our TwiML response
        resp = MessagingResponse()

        # Initialize zipName and prompt if they are not already in the session
        if 'zipName' not in request.session:
            request.session['zipName'] = '11055e45-85e8-49c7-ab5c-f160d1733d88.zip'
        if 'prompt' not in request.session:
            request.session['prompt'] = 'Reply in 10 words to your disciple'

        # Determine the right reply for this message
        if body == 'Hello' or body == "Switch":
            # Send a message to the user to pick a mentor
            resp.message("Greetings! Please select a mentor to engage with:\n1. Krishna\n2. Steve Jobs\n3. Nietzsche\n4. Newton\n5. Napoleon\nType the corresponding number to select your mentor.")
            # Set the session state to indicate that we are waiting for the user's choice
            request.session['waiting_for_choice'] = True
        elif request.session.get('waiting_for_choice'):
            # User is expected to make a choice
            if body in ['1', '2', '3', '4', '5']:
                # User made a valid choice, update zipName and prompt based on the choice
                mentor_mapping = {
                    '1': ('11055e45-85e8-49c7-ab5c-f160d1733d88.zip', 'Reply in 10 words to your disciple'),
                    '2': ('1c16de68-d364-4dd2-bd47-7ad58bce3a60.zip', 'Reply in 10 words to an entrepreneur'),
                    '3': ('03101274-9092-472a-8c0c-89295c0c2c0c.zip', 'You are Zarathustra.Reply in 10 words to your student'),
                    '4': ('5af3a21b-6a1b-4caa-95fb-9a3387130960.zip', 'Reply in 10 words to a science student'),
                    '5': ('26623868-69c1-49cf-be37-4344eea7a688.zip', 'Reply in 10 words like you were a mentor')
                }
                zipName, prompt = mentor_mapping[body]
                request.session['zipName'] = zipName
                request.session['prompt'] = prompt
                result = get_result_from_query(body, zipName, prompt)
                resp.message(result)                                                
                
            else:
                # User made an invalid choice
                resp.message('Invalid choice. Please pick a mentor by entering a number from 1 to 5.')
            # Reset the session state
            request.session.pop('waiting_for_choice', None)
        elif body == 'Bye':
            # User wants to end the conversation
            resp.message("Goodbye")
        else:
            # No specific action based on the user's input
            result = get_result_from_query(body, request.session['zipName'], request.session['prompt'])
            resp.message(result)

        print(f"Response sent: {str(resp)}")  # Add this print statement to check the response before returning

        return HttpResponse(str(resp), content_type='application/xml')
    else:
        print("Error: Only POST requests are allowed for this endpoint")
        return JsonResponse({'error': 'Only POST requests are allowed for this endpoint'}, status=405)
    
# # add new entity to predefined model
class AddEntityToModelView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AddEntitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tenant_id = serializer.validated_data['tenant_id']
        tenant = Tenant.objects.filter(id=tenant_id).first()
        if not tenant:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

        model_name = serializer.validated_data['model_name']
        model_class = self.get_model_class(model_name)
        if not model_class:
            return Response({"error": "Invalid model name"}, status=status.HTTP_400_BAD_REQUEST)

        new_fields = serializer.validated_data['new_fields']
        self.add_fields_to_model(model_class, new_fields)

        return Response({"success": True, "message": "Fields added successfully"}, status=status.HTTP_201_CREATED)

    def get_model_class(self, model_name):
        try:
            return apps.get_model('simplecrm', model_name)
        except LookupError:
            return None

    def add_fields_to_model(self, model_class, new_fields):
        with connection.schema_editor() as schema_editor:
            for field_name, field_type in new_fields.items():
                if not hasattr(model_class, field_name):
                    if field_type == 'string':
                        field_instance = models.CharField(max_length=255, null=True, blank=True)
                    elif field_type == 'integer':
                        field_instance = models.IntegerField(null=True, blank=True)
                    elif field_type == 'text':
                        field_instance = models.TextField(null=True, blank=True)
                    elif field_type == 'boolean':
                        field_instance = models.BooleanField(null=True, blank=True)
                    elif field_type == 'date':
                        field_instance = models.DateField(null=True, blank=True)
                    else:
                        return Response({"error": "Unsupported field type"}, status=status.HTTP_400_BAD_REQUEST)

                    field_instance.contribute_to_class(model_class, field_name)
                    schema_editor.add_field(model_class, field_instance)

    def update_model_instance(self, model_class, field_name, field_instance):
        for instance in model_class.objects.all():
            setattr(instance, field_name, None)
            instance.save()


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Account # Import your predefined models
from contacts.models import  Contact
from .serializers import AddEntitySerializer

# class AddEntityToPredefinedModelView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = AddEntitySerializer(data=request.data)
#         if serializer.is_valid():
#             tenant_id = serializer.validated_data.get('tenant_id')
#             model_name = serializer.validated_data.get('model_name')
#             entity_data_list = serializer.validated_data.get('entity_data')

#             # Validate tenant_id and model_name (assuming they are valid)

#             # Check if the model_name corresponds to a predefined model
#             if model_name not in ['Account', 'Contact']:  # Update with your predefined models
#                 return Response({"error": "Invalid model name"}, status=status.HTTP_400_BAD_REQUEST)

#             # Add entities to the predefined model based on the tenant ID
#             try:
#                 if model_name == 'Account':
#                     for entity_data in entity_data_list:
#                         account = Account.objects.create(tenant_id=tenant_id, **entity_data)
#                         # Handle any additional logic as needed
#                 elif model_name == 'Contact':
#                     for entity_data in entity_data_list:
#                         contact = Contact.objects.create(tenant_id=tenant_id, **entity_data)
#                         # Handle any additional logic as needed

#                 return Response({"success": True, "message": "Entities added successfully"}, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class AddEntityToPredefinedModelView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = AddEntitySerializer(data=request.data)
#         if serializer.is_valid():
#             tenant_id = serializer.validated_data.get('tenant_id')
#             model_name = serializer.validated_data.get('model_name')
#             entity_data_list = serializer.validated_data.get('entity_data')

#             # Validate tenant_id and model_name (assuming they are valid)

#             # Check if the model_name corresponds to a predefined model
#             if model_name not in ['Account', 'Contact']:  # Update with your predefined models
#                 return Response({"error": "Invalid model name"}, status=status.HTTP_400_BAD_REQUEST)

#             # Add entities to the predefined model based on the tenant ID
#             try:
#                 if model_name == 'Account':
#                     for entity_data in entity_data_list:
#                         name = entity_data.get('name')
#                         data_type = entity_data.get('data_type')
#                         value = entity_data.get('value')

#                         # Handle different data types and create entities accordingly
#                         if data_type == 'string':
#                             account = Account.objects.create(tenant_id=tenant_id, name=name, string_field=value)
#                         elif data_type == 'integer':
#                             account = Account.objects.create(tenant_id=tenant_id, name=name, integer_field=value)
#                         # Add conditions for other data types as needed

#                         # Handle any additional logic as needed
#                 elif model_name == 'Contact':
#                     # Similar logic for Contact model
#                     pass

#                 return Response({"success": True, "message": "Entities added successfully"}, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)