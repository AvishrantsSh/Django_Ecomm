from django.shortcuts import render
from .models import Product_List
from django.core import serializers
import json

def Products(request):
    records_all = Product_List.objects.all()
    record_list = serializers.serialize('json', records_all)
    record_list = json.loads(record_list)
    for d in record_list:
        del d['model']

    return render(request, 
                'product_list.html',
                {'data':record_list},
                )

def Product_Dscr(request, pk):
    record = Product_List.objects.get(id=pk)
    
    return render(request, 
                'product_dscr.html',
                {'data':record},
                )
# Create your views here.
