from django.shortcuts import render, redirect
from .models import Product_List, Seller, Cart
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db.models import Q
from .forms import DocumentForm, DocFileForm
from django.contrib.auth import get_user_model
import json
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Search wala scene
from search.main import Indexer
search = Indexer()
# End of Search wala scene

User = get_user_model()
def HomeView(request):
    list_all = Product_List.objects.all()
    if list_all:
        product = [x for x in list_all.order_by("-rating") if x.total_ratings > 10000][:10]
        trending = [x for x in list_all.order_by("-total_ratings") if x.total_ratings > 1631200][:10]
        latest = [x for x in list_all.order_by("-total_ratings") if x.total_ratings < 1500 and x.rating > 4][:10]
        return render(request, 'home.html', {'best': product[1:],
                                         'trending': trending[1:],
                                         'latest': latest[1:],
                                         'bestproduct': product[0],
                                         'trendingproduct': trending[0],
                                         'latestproduct': latest[0],
                                         'seller': list(Seller.objects.all())[0]})
    else:
        return render(request, 'home.html', {'best': None,
                                         'trending': None,
                                         'latest': None,
                                         'bestproduct': None,
                                         'trendingproduct': None,
                                         'latestproduct': None,
                                         'seller': None})

def populate():
    lst = list(Product_List.objects.all())
    lst2 = [['id','name']]
    for i in lst:
        tmp = str(i.id)
        lst2.append([tmp, i.name])
    search.populate_index("index", lst2)

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
            address = json.dumps(address)
            newdoc = Seller(
                            id = request.user.id,
                            bs_name = request.POST['bs_name'],
                            bs_category = request.POST['bs_category'],
                            bank_ac = request.POST['bank_ac'],
                            gst_no = request.POST['gst_no'],
                            pan_no = request.POST['pan_no'],
                            address = address,
                            )
            newdoc.save()
            return redirect('home')
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
    if request.user.is_authenticated:
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
                try:
                    cat = Seller.objects.get(id = request.user.id).bs_category
                except:
                    return redirect('404')

                if cat == "Literature and Stationary":
                    Product_List.objects.filter(seller=request.user.id).delete()
                    # try:
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
                    # except:
                    #     return JsonResponse({"error":"Bad Request"})
                else:
                    return JsonResponse({"error":"Bad Request"})
                    
                return JsonResponse({"success":True})
        else:
            form = DocFileForm() # A empty, unbound form
        
        return render(request,'sheet_upload.html',{'form': form})
    
    return redirect('404')

def put(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            with open('core/tmp.json') as f:
                data = json.loads(f.read())
            for i in data["Data"]:
                Product_List(
                    id = i["id"],
                    name = i["name"],
                    brand = i["brand"],
                    base_price = i["base_price"],
                    rating = i["rating"],
                    total_ratings= i ["total_ratings"],
                    stock = i["stock"],
                    description = i["description"],
                    additional = i["additional"],
                    seller = request.user.id,
                ).save()
        return redirect('404')

def get_dt(request):
    records = Product_List.objects.all()
    record_list = serializers.serialize('json', records)
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
    product = [x for x in Product_List.objects.filter(seller = pk).order_by("-rating") if x.total_ratings > 100][:10]
    trending = [x for x in Product_List.objects.filter(seller = pk).order_by("total_ratings") if x.rating > 4 and x.total_ratings > 10][:10]
    latest = [x for x in Product_List.objects.filter(seller = pk).order_by("total_ratings")][:10]
    return render(request,
                  'seller.html',
                  {'seller': obj, 'best': product, 'trending': trending, 'latest': latest})   

def Product_Dscr(request, pk):
    record = Product_List.objects.get(id=pk)
    slr = Seller.objects.get(id = record.seller)
    return render(request, 
                'product_dscr.html',
                {'data':record,'seller':slr}
                )

def Profile(request):
    try:
        seller = Seller.objects.get(id = request.user.id)
        return render(
                        request,
                        'seller_home.html',
                        {'seller': seller, 'base': "{0}://{1}".format(request.scheme, request.get_host())}
                        )
    except Seller.DoesNotExist:
        # try:
        usr = User.objects.get(id = request.user.id)
        return render(
                        request,
                        'profile.html',
                        {'base_user':usr}
                        )
        # except:
        #     return redirect('404')

def Products(request):
    try:
        seller_pk = request.GET["id"] if request.GET["id"] != "None" else None
    except:
        seller_pk = None
    try:
        sort = request.GET["sort"] if request.GET["sort"] != "None" else None
        sort = sort if sort in ["price_asc","price_dsc","rating", "trend", "fresh", "most"] else "rating"
    except:
        sort = "rating"
    try:
        product = request.GET["product"] if request.GET["product"] != "None" else None 
    except:
        product = None
    try:
        lang = request.GET["lang"] if request.GET["lang"] != "None" else None
        lang = None if lang == "all" else lang
    except:
        lang = None

    lst = ["Scify", "Adventure", "Mystery", "Infotainment"]
    res = []
    for i in lst:
        try:
            if request.GET[i]:
                res.append(i)
        except:
            pass

    # Ah Snap...Here we go again
    if seller_pk:
        if product:
            ret_list = search.index_search(product)
            object_list = Product_List.objects.filter(id__in = ret_list, seller = seller_pk)
        else:
            object_list = Product_List.objects.filter(seller = seller_pk)
    else:
        if product:
            ret_list = search.index_search(product)
            object_list = Product_List.objects.filter(id__in = ret_list)
        else:
            object_list = Product_List.objects.all()
    
    lang_list = []
    cat_list = []
    for x in object_list:
        lang_list.append(json.loads(x.additional)['language'])
        cat_list.append(x.category)
    
    lang_list = list(set(lang_list))
    cat_list = list(set(cat_list))
    cat_list.sort()
    lang_list.sort()
    
    # Sorter 
    if sort == "price_asc":
        object_list = object_list.order_by('base_price')
    elif sort=="price_dsc":
        object_list = object_list.order_by('-base_price')
    elif sort=="rating":
        object_list = object_list.order_by('-rating')
    elif sort=="trend":
        object_list = [x for x in object_list.order_by('total_ratings') if x.rating > 4 and x.total_ratings > 10]
    elif sort=="fresh":
        object_list = [x for x in object_list.order_by('total_ratings')]
    elif sort=="most":
        object_list = [x for x in object_list.order_by('-total_ratings')]
    
    #Cat-Filter
    if res:
        object_list = list(object_list.filter(category__in = res))
    
    #Lang-Filter
    if lang:
        object_list = [x for x in object_list if json.loads(x.additional)['language'] == lang]

    # tmp = object_list.all()
    if not object_list:
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
                {'found':True,
                'page': page,
                'products': products,
                'search':product,
                'sid':seller_pk,
                'total': len(object_list),
                'sort_type': sort,
                'valid_cat': cat_list,
                'valid_lang': lang_list,
                'category': res,
                'lang':lang,
                })

def Add_Cart(request):
    if request.method == 'POST':
        pk = None
        if request.user.is_authenticated:
            if "add" in request.POST.keys():
                pk = request.POST["add"]
                if pk is not None:
                    try:
                        item = Cart.objects.get(customer_id=request.user.id, product_id=pk, status="Cart")
                        item.nos += 1
                        item.save()
                    except:
                        Cart(customer_id=request.user.id, product_id=pk, status="Cart").save()
                    return JsonResponse({'success': "True"})
       
    return JsonResponse({'error': True})

def CartView(request):
    if request.method == "POST":
        if "remove" in request.POST.keys():
            pk = request.POST["remove"]
            if pk is not None:
                try:
                    Cart.objects.get(customer_id=request.user.id, product_id=pk, status="Cart").delete()
                except:
                    return redirect('404')
                
        elif "up" in request.POST.keys():
            pk = request.POST["up"]
            if pk is not None:
                try:
                    item = Cart.objects.get(customer_id=request.user.id, product_id=pk, status="Cart")
                    item.nos += 1
                    tmp = item.nos
                    item.save()
                    # return JsonResponse({'success':True, 'val': tmp})
                except:
                    return redirect('404')
                    # return JsonResponse({'error':True})

        elif "down" in request.POST.keys():
            pk = request.POST["down"]
            if pk is not None:
                try:
                    item = Cart.objects.get(customer_id=request.user.id, product_id=pk, status="Cart")
                    if item.nos == 1:
                        item.delete()
                        tmp = 0
                    else:
                        item.nos -= 1
                        tmp = item.nos
                        item.save()
                    # return JsonResponse({'success':True, 'val': tmp})
                except:
                    return redirect('404')
                    # return JsonResponse({'error':True})

    cart = Cart.objects.filter(customer_id = request.user.id, status="Cart").order_by('-date')
    tmp = []
    for x in cart:
        tmp.append([Product_List.objects.get(id = x.product_id), x.nos]) 
    return render(request, 'cart.html',{'items': tmp})

def populate_db(request):
    populate()
    return redirect('home')
# Create your views here.
