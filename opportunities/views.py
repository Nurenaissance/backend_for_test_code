from django.shortcuts import render
from rest_framework import generics
from .models import Opportunity
from .serializers import OpportunitySerializer
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from .utils import calculate_rfm_metrics


from datetime import datetime, timedelta,date
from django.db.models import Count
from .models import Contact , Account
from leads.models import Lead
from calls.models import calls
from interaction.models import Interaction
from meetings.models import meetings
from campaign.models import Campaign
from django.contrib.auth import get_user_model

# Create your views here.

class OpportunityListAPIView(generics.ListCreateAPIView):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    #permission_classes = (IsAdminUser,)

# views.py


def rfm_analysis(request):
    customers = Opportunity.objects.all().values_list('account', flat=True).distinct()
    rfm_data = []
    for customer_id in customers:
        customer_opportunities = Opportunity.objects.filter(account_id=customer_id)
        recency, frequency, monetary = calculate_rfm_metrics(customer_opportunities)
        rfm_data.append({'customer_id': customer_id, 'recency': recency, 'frequency': frequency, 'monetary': monetary})
    return JsonResponse(rfm_data, safe=False)


CustomUser = get_user_model()

def get_report_by_id(request, report_id):

    report_id_to_function = {
        'total_leads': get_total_leads,
        'this_month_leads': get_new_leads_this_month,
        'converted_leads':get_converted_leads,
        'lead_source':get_leads_by_source,
        'total_calls': get_calls_report_data,
        'total_opportunities': get_opportunity_report_data,
        'total_meetings': get_meetings_report_data,
        'top_users': get_top_users, 
        'Contact_mailing_list':get_contact_address,
        'call_email':get_calls_and_emails,
        'total_campaign':get_total_campaign,
        'total_interaction':get_interaction_total,
        'today_lead':get_leads_by_today,
        'leads_account_name':get_leads_by_account_name,
        'campaign_status':get_campaign_status,
  
    }
    report_function = report_id_to_function.get(report_id)

    if not report_function:
        return JsonResponse({'error': 'Invalid report type'}, status=400)

    try:
        report_data = report_function()
        return JsonResponse(report_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
#--------leads-----

def get_total_leads():
        leads = Lead.objects.all()
        report_data = {'total_leads': leads.count(), 'leads': list(leads.values())}
        return report_data

def get_new_leads_this_month():
    today = datetime.today()
    start_date = today.replace(day=1) 
    end_date = today.replace(day=1) + timedelta(days=32) 

    new_leads_count = Lead.objects.filter(createdOn__gte=start_date, createdOn__lt=end_date).count()

    report_data = {'new_leads_count': new_leads_count}
    return report_data

def get_converted_leads():
    converted_leads = Lead.objects.filter(status='converted')
    return list(converted_leads.values('id', 'first_name', 'last_name','phone','status','account'))

def get_leads_by_source():
    lead_source = Lead.objects.all()
    report_data = {'total lead':lead_source.count(), 'source':list(lead_source.values('id', 'source','email','createdOn','createdBy','account_name','first_name','last_name'))}
    return report_data

def get_leads_by_today():
    today_date = date.today()
    leads_today = Lead.objects.filter(createdOn__date=today_date)
    report_data = {'total_today_leads':leads_today.count(), 'today_leads':list(leads_today.values('email','phone','source','status')) }
    return report_data
def get_leads_by_account_name():
    Account_name = Lead.objects.filter()
    report_data = {'total_leads_account_name':Account_name.count(),'leads_account_name':list(Account_name.values('id','account_name'))}
    return report_data

#-----end leads------

def get_calls_report_data():
    call = calls.objects.all()
    report_data = {'total_calls': call.count(), 'calls': list(call.values())}
    return report_data

def get_opportunity_report_data():
    Opportunities = Opportunity.objects.all()
    report_data = {'total_opportunity': Opportunities.count(), 'opportunity':list(Opportunities.values())}
    return report_data

def get_meetings_report_data():
    Meeting  = meetings.objects.all()
    report_data = {'total_meeting': Meeting.count(),'meetings':list(Meeting.values())}
    return report_data
def get_top_users():
    top_users = CustomUser.objects.order_by('-date_joine')[:10]
    report_data = {'top_users': list(top_users.values('id', 'username', 'date_joined'))}
    return report_data

def get_contact_address():
    contacts = Contact.objects.all()
    report_data = {'total contacts': contacts.count(), 'Contacts': list(contacts.values('id','first_name','last_name', 'address'))}
    return report_data

def get_calls_and_emails():
    call = calls.objects.all()
    email = Contact.objects.all()

    call_data = list(call.values('id','call_to'))
    email_data = list(email.values('id','first_name'))
    report_data = {'total calls': call.count(), 'calls':call_data, 'total emails': email.count(), 'eamils':email_data}
    return report_data

def get_total_campaign():
    total_campaign = Campaign.objects.all()
    report_data = {'total campaign':total_campaign.count(), 'campaign':list(total_campaign.values('campaign_owner','campaign_name'))}
    return report_data

def get_campaign_status():
    status = Campaign.objects.all()
    report_data = {'total_status':status.count(), 'status':list(status.values('id','status','campaign_owner','campaign_name','start_date','end_date'))}
    return report_data

def get_interaction_total():
    total_interaction = Interaction.objects.all()
    report_data = {'total_interaction':total_interaction.count(), 'interaction': list(total_interaction.values('id','notes','entity_type'))}
    return report_data