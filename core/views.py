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
            address = {
                "Address1":request.POST["addr1"],
                "Address2":request.POST["addr2"],
                "District":request.POST["district"],
                "State":request.POST["state"],
                "Country":request.POST["country"],
                "Pincode":request.POST["pincode"]
            }
            newdoc = Seller(
                            id = request.user.id,
                            bs_name = request.POST['bs_name'],
                            bs_category = request.POST['bs_category'],
                            bank_ac = request.POST['bank_ac'],
                            gst_no = request.POST['gst_no'],
                            pan_no = request.POST['pan_no'],
                            address = json.dumps(address),
                            pan_card = request.FILES['pan_card'],
                            )
            newdoc.save()
            return redirect('confirm')
    else:
        form = DocumentForm() # A empty, unbound form
    
    review=False
    try:
        obj = Seller.objects.get(id=request.user.id)
        review = True if obj.status == "Reviewing" else False
    except Seller.DoesNotExist:
        return render(request,'seller_register.html',{'form': form, 'review': review, 'complete':False})
    
    return render(request,'seller_register.html',{'form': form, 'review':review, 'complete':True})
# Create your views here.
