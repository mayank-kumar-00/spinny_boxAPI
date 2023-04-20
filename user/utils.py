from datetime import datetime, timedelta
from rest_framework import status
from django.db.models import F
from .models import Box
from .keys import *

def validate_data(user, new_box, data):
    leng = data.get(LENGTH, new_box.length)
    bres = data.get(BREADTH, new_box.breadth)
    heig = data.get(HEIGHT, new_box.height)
    week_start = datetime.today()
    week_start -= timedelta(days=week_start.weekday())
    week_end = week_start + timedelta(days=7)
    all_box = Box.objects.filter(created_at__date__gte=week_start.date(), 
                            created_at__date__lte=week_end.date()).exclude(id=new_box.id)
    
    if all_box.count() >= L1:
        return False, 'You have reached the maximum limit' , status.HTTP_429_TOO_MANY_REQUESTS
    
    if all_box.filter(user=user).count() >= L2:
        return False, 'You have reached the maximum limit' , status.HTTP_429_TOO_MANY_REQUESTS
    
    total_box = all_box.count()
    
    areas = list(all_box.annotate(area=F('length')*F('breadth')).values_list('area', flat=True)) + [leng * bres]
    if sum(areas) / ( total_box + 1) >= L1:
        return False, 'Area exceed the limit' , status.HTTP_400_BAD_REQUEST
    
    user_box = all_box.filter(user=user).annotate(volume=F(LENGTH)*F(BREADTH)*F(HEIGHT))
    total_box = user_box.count()
    volumes = list(user_box.annotate(volume=F('length')*F('breadth')*F('height')).values_list('volume', flat=True)) + [leng * bres * heig]
    
    if sum(volumes) / ( total_box + 1) >= V1:
        return False, 'Volume exceed the limit' , status.HTTP_400_BAD_REQUEST
    return True, True, True