from django.http import JsonResponse
from accounts.models import * 
from leads.models import Lead
from contacts.models import * 
from opportunities.models import * 
from django.core.exceptions import FieldError

def recent_request(request, model_name):
    try:
        model_class = None
        if model_name == 'leads':
            model_class = Lead
        elif model_name == 'accounts':
            model_class = Account
        elif model_name == 'opportunities':
            model_class = Opportunity
        elif model_name == 'contacts':
            model_class = Contact
        else:
            return JsonResponse({'message': 'Invalid model name.'}, status=400)
<<<<<<< HEAD
        
        vals = model_class.objects.all().order_by('createdOn')
        
=======

        vals = model_class.objects.all().order_by('createdOn')

>>>>>>> ebcf565080fc7cd921aa134b69187bf116a17d51
        created_on_date = request.GET.get('created_on')
        if created_on_date:
            try:
                vals = vals.filter(createdOn=created_on_date)
            except FieldError:
                return JsonResponse({'message': 'createdOn field not found in the model.'}, status=400)

        data = [
            {
                'id': val.id,
                'created_on': val.createdOn,
            }
            for val in vals
        ]

        return JsonResponse(data, safe=False)
    except Exception as e:
        print("Error:", e)
<<<<<<< HEAD
        return JsonResponse({'message': 'An error occurred.'}, status=500)
=======
        return JsonResponse({'message': 'An error occurred.'}, status=500)
>>>>>>> ebcf565080fc7cd921aa134b69187bf116a17d51
