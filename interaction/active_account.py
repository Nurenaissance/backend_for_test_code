from django.db import models
from django.db.models import Count
from accounts.models import Account
from contacts.models import Contact
from django.db.models.functions import Coalesce
from leads.models import Lead
from django.db.models import Count, Sum, OuterRef, Subquery, Value
from django.http import JsonResponse
from interaction.models import Interaction
from accounts import serializers as accser
from contacts import serializers as conser
AccountSerializer=accser.AccountSerializer
ContactSerializer=conser.ContactSerializer

LEAD_STATUS = [
    ('assigned', 'Assigned'),
    ('in process', 'In Process'),
    ('converted', 'Converted'),
    ('recycled', 'Recycled'),
    ('dead', 'Dead')
]

def get_most_active_accounts(request):
    try:
        # Annotate accounts with interaction counts
        accounts = Account.objects.annotate(
            interaction_count=Coalesce(
                Subquery(
                    Interaction.objects.filter(
                        entity_type__model='account',
                        entity_id=OuterRef('pk')
                    ).values('entity_id').annotate(count=Count('id')).values('count'),
                    output_field=models.IntegerField()
                ), 
                Value(0),
                output_field=models.IntegerField()
            )
        ).order_by('-interaction_count')  # Order by interaction count in descending order

        # Serialize the account data
        serializer = AccountSerializer(accounts, many=True)

        # Prepare response data with interaction count added to each account
        response_data = []
        for account, serialized_data in zip(accounts, serializer.data):
            serialized_data['interaction_count'] = account.interaction_count
            response_data.append(serialized_data)

        return JsonResponse({
            'most_active_accounts': response_data
        }, safe=False)
    except Exception as e:
        print("Error:", e)
        return JsonResponse({'message': 'An error occurred.'}, status=500)
    
   
def get_most_active_contacts(request):
    try:
        # Annotate contacts with interaction counts
        contacts = Contact.objects.annotate(
            interaction_count=Coalesce(
                Subquery(
                    Interaction.objects.filter(
                        entity_type__model='contact',
                        entity_id=OuterRef('pk')
                    ).values('entity_id').annotate(count=Count('id')).values('count'),
                    output_field=models.IntegerField()
                ), 
                Value(0),
                output_field=models.IntegerField()
            )
        ).order_by('-interaction_count')  # Order by interaction count in descending order

        # Serialize the contact data
        serializer = ContactSerializer(contacts, many=True)

        # Prepare response data with interaction count added to each contact
        response_data = []
        for contact, serialized_data in zip(contacts, serializer.data):
            serialized_data['interaction_count'] = contact.interaction_count
            response_data.append(serialized_data)

        return JsonResponse({
            'most_active_contacts': response_data
        }, safe=False)
    except Exception as e:
        print("Error:", e)
        return JsonResponse({'message': 'An error occurred.'}, status=500)

def get_lead_summation(request):
    try:
        stages = Lead.objects.values('status').annotate(
            total_amount=Sum('opportunity_amount'),
            lead_count=Count('id')
        ).order_by('status')
        
        status_dict = {status[0]: {'total_amount': 0, 'lead_count': 0} for status in LEAD_STATUS}

        for stage in stages:
            status_dict[stage['status']] = {
                'total_amount': stage['total_amount'],
                'lead_count': stage['lead_count']
            }

        stages_with_all_statuses = [
            {'status': status, 
             'total_amount': data['total_amount'], 
             'lead_count': data['lead_count']
            }
            for status, data in status_dict.items()
        ]
        
        total_amount = Lead.objects.aggregate(total_amount=Sum('opportunity_amount'))['total_amount']

        return JsonResponse({
            'lead_sum': {
                'stages': stages_with_all_statuses,
                'total_amount': total_amount,
            }
        }, safe=False)
    except Exception as e:
        print("Error:", e)
        return JsonResponse({'message': 'An error occurred.'}, status=500)