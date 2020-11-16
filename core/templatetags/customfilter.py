from django import template
from django.contrib.auth import get_user_model
from core.models import Seller
register = template.Library()

@register.filter
def active(s_id):
    resp = False
    try:
        obj = Seller.objects.get(id = s_id)
        resp = True if obj.status == "Active" else False
    except Seller.DoesNotExist:
        resp = False
        
    return resp
       
