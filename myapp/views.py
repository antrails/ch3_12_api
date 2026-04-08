from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.core.paginator import Paginator


# Create your views here.

def search_list(request):
    if 'cname' in request.GET:
        cname = request.GET['cname']
        print(cname)
        result_list = students.objects.filter(cname__contains=cname)
    else:
        result_list = students.objects.all().order_by('cid')


    for item in result_list:
        print(model_to_dict(item))
    # return HttpResponse("hiiii")
    # result_list = [] #模擬沒有資料的情況下 ，讓errormessage有值
    errormessage = ""
    if not result_list:
        errormessage = "No data found."
    # return render(request, 'search_list.html', locals())
    return render(request, 'search_list.html', {'result_list': result_list, 'errormessage': errormessage})


def search_name(request):
    return render(request, 'search_name.html') #沒有變數要拋 所以沒有locals不影響

# def index(request):
#     result_list = students.objects.all().order_by('cid')
#     for item in result_list:
#         print(model_to_dict(item))
#         if item.csex == 'M':
#             item.csex = '男'
#         else:
#             item.csex = '女'
#     datacount = len(result_list)
#     print(f"Total data count:{datacount}")
#     status = True
#     errormessage=""
#     if not result_list:
#         status = False
#         errormessage = "No data found."
#     # return HttpResponse("Hii")
#     return render(request, 'index.html',
#                    {'result_list': result_list, 'status': status, 'errormessage': errormessage , 'datacount':datacount})

def post(request):
    if request.method == "POST":
        cname = request.POST.get('cname')
        csex  = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr  = request.POST.get('caddr')
        print(f"Recevied Post data : cname:{cname},csex:{csex},cbirthday:{cbirthday},cemail:{cemail},cphone:{cphone},caddr:{caddr}")
        add = students(cname = cname, csex = csex,cbirthday = cbirthday,cemail = cemail,cphone=cphone,caddr=caddr)
        add.save()
        # return HttpResponse("已送出 POST 請求")
        return redirect('index')
    else:
        return render (request,'post.html')
    


def edit(request,id):
    print(id)
    if request.method == 'POST':
        cname = request.POST.get('cname')
        csex  = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr  = request.POST.get('caddr')
        print(f"Recevied Post data : cname:{cname},csex:{csex},cbirthday:{cbirthday},cemail:{cemail},cphone:{cphone},caddr:{caddr}")
        update = students.objects.get(cid=id)
        update.cname = cname
        update.csex = csex
        update.cbirthday = cbirthday
        update.cemail = cemail
        update.cphone = cphone
        update.caddr = caddr
        update.save()
        return redirect('index')
        # return HttpResponse("已送出POST請求")
    else:
        obj_data = students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        # return HttpResponse("Hiiii")
        return render (request,'edit.html',{'obj_data':obj_data})
    
def delete(request,id):
    print(id)
    if request.method == 'POST':
        delete_data = students.objects.get(cid=id)
        delete_data.delete()
        return redirect('index')
    else:
        obj_data = students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        return render(request,'delete.html',{'obj_data':obj_data})
    
from django.db.models import Q


def index(request):
    site_search = request.GET.get("site_search", "").strip()

    if site_search:
        keywords = site_search.split()
        print(keywords)

        query = Q()

        for keyword in keywords:
            keyword_query = (
                Q(cid__icontains=keyword) |
                Q(cname__icontains=keyword) |
                Q(cbirthday__icontains=keyword) |
                Q(cemail__icontains=keyword) |
                Q(cphone__icontains=keyword) |
                Q(caddr__icontains=keyword)
            )
            query |= keyword_query 

        resultList = students.objects.filter(query).order_by('cid')

    else:
        resultList = students.objects.all().order_by('cid')

    for item in resultList:
        print(model_to_dict(item))

    data_count = resultList.count()
    print(f"Total data count: {data_count}")

    status = resultList.exists()
    errormessage = "" if status else "No data found"
    #分頁設定 每頁顯示2筆資料
    paginator = Paginator(resultList, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_number)
    for item in page_obj:
        print(model_to_dict(item))

    return render(request, 'index.html', {
        'resultList': resultList,
        'data_count': data_count,
        'status': status,
        'errormessage': errormessage,
        'page_obj': page_obj
    })

from django.http import JsonResponse
def getAllItems(request):
    resultObject = students.objects.all().order_by('cid')
    # for item in resultList:
    #     print(type(item))
    resultList = list(resultObject.values())
    # print(type(resultList   ))
    # for item in resultList:
    #     print(type(item))
    # return HttpResponse("Hello")
    return JsonResponse(resultList,safe=False) #safe=True時=只允許傳入dict , False時只允許非dict

def getItem(request,id):

    try:
        obj = students.objects.get(cid=id)
        print(type(obj))  #這時候是物件 要轉成字典
        res = model_to_dict(obj) 
        # return HttpResponse("Hii")
        return JsonResponse(res,safe=False)
    except:
        return JsonResponse({"error":"Item not found"},status=404)



from django.views.decorators.csrf import csrf_exempt
#停止csrf驗證 讓外部程式也可以呼叫這個api
@csrf_exempt    
def createItem(request):
    try:
        if request.method == "GET":
            cname = request.GET['cname']
            csex  = request.GET['csex']
            cbirthday = request.GET['cbirthday']
            cemail = request.GET['cemail']
            cphone = request.GET['cphone']
            caddr  = request.GET['caddr']
            print(f"GET data: cname={cname},csex={csex},cbirthday={cbirthday},cemail={cemail},cphone={cphone},caddr={caddr}")
            
        
        elif request.method == "POST":
            cname = request.POST['cname']
            csex  = request.POST['csex']
            cbirthday = request.POST['cbirthday']
            cemail = request.POST['cemail']
            cphone = request.POST['cphone']
            caddr  = request.POST['caddr']
            print(f"POST data: cname={cname},csex={csex},cbirthday={cbirthday},cemail={cemail},cphone={cphone},caddr={caddr}")
        try:
            add = students(cname = cname, csex = csex,cbirthday = cbirthday,cemail = cemail,cphone=cphone,caddr=caddr)
            add.save()
            return JsonResponse({"message":"Item created successfully"},status=201)
        except:
            return JsonResponse({"error":"Item created error"},status=500)

    except:
        return JsonResponse({"error":"Invalid data"},status=400)    
    

@csrf_exempt 
def updateItem(request,id):
    print(f"id={id}")
    try:
        if request.method == "GET":
            cname = request.GET['cname']
            csex  = request.GET['csex']
            cbirthday = request.GET['cbirthday']
            cemail = request.GET['cemail']
            cphone = request.GET['cphone']
            caddr  = request.GET['caddr']
            print(f"GET data: cname={cname},csex={csex},cbirthday={cbirthday},cemail={cemail},cphone={cphone},caddr={caddr}")
            


        elif  request.method == "POST":
            cname = request.POST['cname']
            csex  = request.POST['csex']
            cbirthday = request.POST['cbirthday']
            cemail = request.POST['cemail']
            cphone = request.POST['cphone']
            caddr  = request.POST['caddr']
            print(f"POST data: cname={cname},csex={csex},cbirthday={cbirthday},cemail={cemail},cphone={cphone},caddr={caddr}")
            
        try:
            update = students.objects.get(cid=id)
            update.cname = cname
            update.csex = csex
            update.cbirthday = cbirthday
            update.cemail = cemail
            update.cphone = cphone
            update.caddr = caddr
            update.save()
            return JsonResponse({"message":"Item update successfully"},status=201)
        except:
            return JsonResponse({"error":"Item created error"},status=500)
    except:
        return JsonResponse({"error":"Invalid data"},status=400)