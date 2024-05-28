from django.db import models
from django.db.models import Count
from accounts.models import Account
from contacts.models import Contact
from django.db.models.functions import Coalesce
from leads.models import Lead
from django.db.models import Count, Sum, OuterRef, Subquery, Value
from django.http import JsonResponse
from interaction.models import Interaction



LEAD_STATUS = [
    ('assigned', 'Assigned'),
    ('in process', 'In Process'),
    ('converted', 'Converted'),
    ('recycled', 'Recycled'),
    ('dead', 'Dead')
]

def most_active_entities(request):
    try:
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
        )

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
        )

        most_active_accounts = [{
            'entity_id': account.id,
            'interaction_count': account.interaction_count
        } for account in accounts]

        most_active_contacts = [{
            'entity_id': contact.id,
            'interaction_count': contact.interaction_count
        } for contact in contacts]

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
        
        total_amount = Lead.objects.aggregate(total_amount=Sum('account_id'))['total_amount']

        return JsonResponse({
            'most_active_accounts': most_active_accounts,
            'most_active_contacts': most_active_contacts,
            'lead_sum': {
                'stages': stages_with_all_statuses,
                'total_amount': total_amount,
            }
        }, safe=False)
    except Exception as e:
        print("Error:", e)
        return JsonResponse({'message': 'An error occurred.'}, status=500)