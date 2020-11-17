from django.shortcuts import render, redirect
from .models import Product_List, Seller
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db.models import Q
from .forms import DocumentForm, DocFileForm
from django.contrib.auth import get_user_model
import json
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

User = get_user_model()

def to_dict(lst):
    key = lst[0]
    del lst[0]
    ans = []
    num = 0
    for i in lst:
        tmp={}
        for j in range(len(key)):
            tmp[str(key[j]).lower()] = i[j]
        ans.append(tmp)
        num += 1
        # if num >= 1000:
        #     break
    return ans

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
        if obj.status == "Active":
            return redirect('profile')
        review= True

    except Seller.DoesNotExist:
        return render(request,'seller_register.html',{'form': form, 'review': review})
    
    return render(request,'seller_register.html',{'form': form, 'review':review})

def Extract_dt(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES['docfile']
            except:
                return JsonResponse({"error":"File not found"})

            if(str(excel_file).split('.')[-1]=="xls"):
                data = xls_get(excel_file, column_limit=10)

            elif(str(excel_file).split('.')[-1]=="xlsx"):
                data = xlsx_get(excel_file, column_limit=10)

            else:
                return JsonResponse({"error":"Invalid File Format"})

            data = data[list(data.keys())[0]]    
            data = to_dict(data)
            cat = Seller.objects.get(id = request.user.id).bs_category

            if cat == "Electronics":
                Product_List.objects.all().delete()
                for i in data:
                    Product_List(
                        name = i["product"],
                        brand = i["author"],
                        base_price = i["price"],
                        stock = i["stock"],
                        description = i["description"] if "description" in i.keys() 
                                                        else "No description provided by Seller",
                        additional = json.dumps({"warranty": i["warranty"]}),
                        seller = request.user.id,
                    ).save()
                    
            elif cat == "Literature and Stationary":
                Product_List.objects.all().delete()
                for i in data:
                    Product_List(
                        name = i["title"],
                        brand = i["publisher"],
                        base_price = i["price"],
                        rating = i["rating"],
                        total_ratings= i ["total ratings"],
                        stock = i["stock"],
                        description = i["description"] if "description" in i.keys() 
                                                        else "No description provided by Seller",
                        additional = json.dumps({"author": i["author"], "pages": i["pages"], "language":i["language"], "publication date":i["publication date"]}),
                        seller = request.user.id,
                    ).save()

            elif cat == "Groceries":
                for i in data:
                    try:
                        Product_List.objects.get(name=i["product"], brand=i["brand"], seller=request.user.id).delete()
                        print("Updating Entry")
                    except Product_List.DoesNotExist:
                        print("Adding New Entry")

                    Product_List(
                        name = i["product"],
                        brand = i["brand"],
                        base_price = i["price"],
                        stock = i["stock"],
                        description = i["description"] if "description" in i.keys() 
                                                        else "No description provided by Seller",
                        additional = json.dumps({"manufactured":i["date of manufacture"], "expiry": i["date of expiry"]}),
                        seller = request.user.id,
                    ).save()
            else:
                return JsonResponse({"error":"Bad Request"})
                
            return JsonResponse({"success":True})
    else:
        form = DocFileForm() # A empty, unbound form
    
    return render(request,'sheet_upload.html',{'form': form})

def get_dt(request):
    records = Product_List.objects.all()
    record_list = serializers.serialize('json', records, fields=('name'))
    data = json.loads(record_list)
    tmp=[]
    for d in data:
        del d['model']
        d['fields']['id'] = d['pk']
        tmp.append(d['fields'])

    cleaned_response = {'Data':tmp}
    json_file=json.dumps(cleaned_response, indent=4, sort_keys=True)
    return HttpResponse(json_file, content_type="text/plain")

def Seller_Landing(request, cat, store, pk):
    try:
        obj = Seller.objects.get(id = pk)
        if obj.bs_name != store or obj.bs_category != cat:
            raise Exception
    except:
        return redirect('404')
    
    return render(request,
                  'seller.html',
                  {'seller': obj})   

def Product_Dscr(request, pk):
    record = Product_List.objects.get(id=pk)
    slr = Seller.objects.get(id = record.seller)
    return render(request, 
                'product_dscr.html',
                {'data':record,'seller':slr}
                )

def Profile(request):
    try:
        slr = Seller.objects.get(id = request.user.id)
        return render(
                        request,
                        'seller_home.html',
                        {'details': slr, 'base': "{0}://{1}".format(request.scheme, request.get_host())}
                        )
    except Seller.DoesNotExist:
        try:
            User.objects.get(id = request.user.id)
            return render(
                            request,
                            'profile.html',
                            {}
                            )
        except:
            return redirect('404')

def Products(request):
    if request.method == "GET":
        try:
            seller_pk = request.GET["id"]
        except:
            seller_pk = None
        try:
            sort = request.GET["sort"]
        except:
            sort = None
        try:
            product = request.GET["product"]
        except:
            product = None
        # Ah Snap...Here we go again
        try:
            if seller_pk:
                object_list = list(Product_List.objects.filter(
                                                                Q(seller=seller_pk) &
                                                                Q(name__icontains = product if product else "")
                                                          
                                                        ).order_by('-rating' if sort is None else "-"+sort))
            
            else:
                object_list = list(Product_List.objects.filter(Q(name__icontains = product if product else "")).order_by('-rating' if sort is None else "-"+sort))
            
        except:
            return render(request,
                    'search.html',
                    {'found':False})

        paginator = Paginator(object_list, 20)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
                
        return render(request,
                    'search.html',
                    {'page': page,
                    'products': products,
                    'search':product
                    })

    return redirect('404')

# Create your views here.
