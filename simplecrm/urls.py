"""simplecrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from accounts import views as aviews 
from leads import views as lviews
from opportunities import views as oviews
from contacts import views as cviews
from meetings import views as mviews
from calls import views as caviews
from interaction import views as inviews
from tasks import views as tviews
from reminder import views as rviews
from simplecrm import Register_login as Reg
from simplecrm import ingestexcel as ingex
from simplecrm import get_column_name as getxcol
from simplecrm import get_user as getuser
from tenant import views as tenview
from campaign import views as campview
from simplecrm.recent_request import recent_request
from interaction.active_account import most_active_entities
from node_temps import views as nviews
from interaction.views import extract_cltv
from opportunities.views import get_report_by_id


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('register/', Reg.register, name='register'),  # Endpoint for user registration
    path('login/', Reg.LoginView.as_view(), name='login'), 
    path(r'accounts/', aviews.AccountListCreateAPIView.as_view(), name='account-list'),
    path('accounts/<int:pk>/', aviews.AccountDetailAPIView.as_view(), name='account-detail'),
    path("active_accounts/",most_active_entities, name="most-active-entites"),
    path(r'leads/', lviews.LeadListCreateAPIView.as_view(), name='lead-list'),
    path('leads/<int:pk>/',lviews.LeadDetailAPIView.as_view(), name='lead-detail'),
    path('request/<str:module_name>/',recent_request, name='recent_request'),
    path(r'opportunities/', oviews.OpportunityListAPIView.as_view(), name='opportunity-list'),
    path('contacts/', cviews.ContactListCreateAPIView.as_view(), name='contact-list-create'),
    path('contacts/<int:pk>/', cviews.ContactDetailAPIView.as_view(), name='contact-detail'),
    path('meetings/', mviews.MeetingListCreateAPIView.as_view(), name='meeting-list-create'),
    path('meetings/<int:pk>/', mviews.MeetingDetailAPIView.as_view(), name='meeting-detail'),
    path('calls/', caviews.callsListAPIView.as_view(), name='calls'), 
    path('interaction/', inviews.InteractionListAPIView.as_view(), name='interaction'),  
    path('tasks/', tviews.TaskListCreateAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', tviews.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'), 
    path('reminders/', rviews.ReminderListAPIView.as_view(), name='reminder-list'),
    path('uploadexcel/', ingex.ImportLeadData, name='excel'),
    path('excel-column/', getxcol.get_excel_columns, name='column_excel'),
    path('get-user/<str:username>/', getuser.get_user_by_username, name='get_user'),
    path('createTenant/', tenview.tenant_list, name='tenant'),
    path('logout/', Reg.LogoutView.as_view(), name='logout'),
    path('campaign/', campview.CampaignViewSet.as_view(), name='campaigns'),
    path('campaign/<int:pk>', campview.CampaignDetailAPIView.as_view(), name='campaigns'),
    path(r'node-templates/', nviews.NodeTemplateListCreateAPIView.as_view(), name='node-template-list-create'),
    path('node-templates/<int:pk>/', nviews.NodeTemplateDetailAPIView.as_view(), name='node-template-detail'),
    path('extract_cltv/<int:entity_type_id>/', extract_cltv, name='extract_cltv'),
    # path ('report/<int:report_id/',get_report_by_id, name='get_report_by_id'),
    path ('r/<str:report_id>/', get_report_by_id, name='get_report_by_id'),
    

   

]