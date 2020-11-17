from django import template
from django.contrib.auth import get_user_model
from core.models import Seller
import json
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

@register.filter
def trim(value):
    return str(value).replace("\n"," ")[:25]+"..." if len(value) > 25 else value

@register.filter
def dtrim(value):
    return str(value)[:40]+"..."

@register.filter
def author(dic):
    return json.loads(dic)["author"]

@register.filter
def pages(dic):
    return json.loads(dic)["pages"]

@register.filter
def date(dic):
    return json.loads(dic)["publication date"]

@register.filter
def language(dic):
    return json.loads(dic)["language"]
       
@register.filter
def authtrim(value):
    if ',' in value:
        value = value.split(',')
    
    if '/' in value:
        value = value.split('/')
    
    else:
        value = [value]
    x = "" if len(value) == 1 else " and more"
    return value[0] + x