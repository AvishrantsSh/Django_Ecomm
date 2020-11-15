from django.shortcuts import render, redirect
from .models import Product_List, Seller
from django.template import RequestContext
from django.core import serializers
from .forms import DocumentForm, DocFileForm
import json
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError

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

def Extract_dt(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES['docfile']
            except MultiValueDictKeyError:
                return redirect('404')
            if(str(excel_file).split('.')[-1]=="xls"):
                data = xls_get(excel_file, column_limit=4)

            elif(str(excel_file).split('.')[-1]=="xlsx"):
                data = xlsx_get(excel_file, column_limit=4)

            else:
                return redirect('404')

            data = data["Sheet1"]    
            del data[0]
            for i in data:
                try:
                    Product_List.objects.get(name=i[0]).delete()
                    print("Updating Entry")
                except Product_List.DoesNotExist:
                    print("Adding New Entry")

                Product_List(
                    name = i[0],
                    brand = i[1],
                    base_price = i[2],
                    stock = i[3],
                    seller = request.user.id,
                ).save()
                
            return redirect('home')
    else:
        form = DocFileForm() # A empty, unbound form
    
    return render(request,'sheet_upload.html',{'form': form})
# Create your views here.
