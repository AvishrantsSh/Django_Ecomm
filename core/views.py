from django.shortcuts import render, redirect
from .models import Product_List, Seller
from django.template import RequestContext
from django.core import serializers
from .forms import DocumentForm
import json

def Seller_reg(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Seller(id_card = request.FILES['id_card'])
            newdoc.save()

            return redirect('home')
    else:
        form = DocumentForm() # A empty, unbound form

    documents = Seller.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'seller_register.html',
        {'documents': documents, 'form': form},
        # context_instance=RequestContext(request)
    )
# Create your views here.
