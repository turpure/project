# -*-coding:utf-8-*-
from django.shortcuts import render, render_to_response
from forms import UserForm, UserFormLogIN, ShopForm
from models import User, Shops, Products, KeyWords, KWProducts
from django.http import HttpResponse, HttpResponseRedirect, Http404,JsonResponse
import json
import datetime
from my_ebay_tools.myshop import update_shop_products, update_keywords_product


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":

        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['user']
            password1 = uf.cleaned_data['password1']
            password2 = uf.cleaned_data['password2']
            if password1 == password2:
                User.objects.create(username=username, password=password1)
                Shops.objects.create(userid=username, feedbackscore=0, curdate=str(datetime.datetime.now()))
                # add one row in shop table
                KeyWords.objects.create(userid=username, curdate=str(datetime.datetime.now()))
                # add one row in keywords table
                response = render(request, 'home.html')
                try:
                    response.delete_cookie('username')
                except Exception as e:
                    print e
                return response
            else:
                return HttpResponse('俩次密码不一样，请重新注册！')
    else:
        uf = UserForm()
        return render(request, 'register.html', {'uf': uf})


def login(request):
    if request.method == "POST":
        uf = UserFormLogIN(data=request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['user']
            password = uf.cleaned_data['password']
            user = User.objects.filter(username__exact=username, password__exact=password)
            if user:
                response = HttpResponseRedirect('/home')
                response.set_cookie('username', username, 3600000)
                return response
            else:
                return HttpResponseRedirect('/home/login')
        else:
            raise Http404
    else:
        uf = UserFormLogIN()
        return render(request, 'login.html', {"uf": uf})


def logout(request):
    response = HttpResponse("Log out!")
    response.delete_cookie('username')
    return response


def dashboard(request):
    return render(request, "dashboard.html")


def shops(request):
    return render(request, "shops.html")


def  remove_all_shops(request):
    if request.method == "POST":
        userid = request.COOKIES.get('username', '')
        if userid:
            ids_string = request.POST.get('ids')
            ids_dict = json.loads(ids_string)
            ids = ids_dict['ids']
            for id in ids:
                Shops.objects.filter(id=id).delete()
            return JsonResponse({"msg":"it works!"})
        else:
            return JsonResponse({"msg":'it fails!'})



def addall(request):
    if request.method == 'POST':
        userid = request.COOKIES.get('username', '')
        if userid:
            data2upload = request.POST.get('data')
            data_json = json.loads(data2upload)
            data = data_json['data']
            curdate = str(datetime.datetime.now())
            if data:
                for row in data:
                    shopname = row['shopname']
                    feedbackscore = row['feedbackscore']                   
                    Shops.objects.create(shopname=shopname, userid=userid, curdate=curdate, feedbackscore=feedbackscore)
                return JsonResponse({'msg':'it works!', 'code':0})
            else:
                return JsonResponse({"msg":"no content", 'code': 2})

    else:
        return JsonResponse({'msg':'noi loggin!', 'code':1})

def get_shops(request):
    userid = request.COOKIES.get('username', '')
    if userid:
        return JsonResponse(dict(data=list(Shops.objects.filter(userid__exact=userid).order_by('-id').values())))


def add_shops(request):
    if request.method == "POST":
        userid = request.COOKIES.get('username', '')
        shopname = request.POST.get('shopname')
        feedbackscore = request.POST.get('feedbackscore')
        curdate = str(datetime.datetime.now())
        # print shopname, feedbackscore
        Shops.objects.create(shopname=shopname, userid=userid, curdate=curdate, feedbackscore=feedbackscore)
        return JsonResponse({'msg': 'It works!'})

    else:
        return JsonResponse({'msg': 'It fails'})


def edit_shops(request):
    if request.method == "POST":
        userid = request.COOKIES.get('username', '')
        if userid:
            id =request.POST.get('id')
            shopname = request.POST.get('shopname')
            feedbackscore = request.POST.get('feedbackscore')
            # print shopname, feedbackscore
            Shops.objects.filter(id=id).update(shopname=shopname, feedbackscore=feedbackscore)
            print "updating...."
            return JsonResponse({'msg': 'It works!'})

    else:
        return JsonResponse({'msg': 'It fails'})


def delete_shops(request):
    if request.method == "POST":
        userid = request.COOKIES.get('username', '')
        if userid:
            id = request.POST.get('id')
            Shops.objects.filter(id=id).delete()
            print "deleting..."
            return JsonResponse({'msg': 'It works!'})

    else:
        return JsonResponse({'msg': 'It fails'})


def update_shops(request):
    if request.method == "POST":
        userid = request.COOKIES.get('username', '')
        if userid:
            shopname = request.POST.get('shopname')
            id = request.POST.get('id')
            Shops.objects.filter(id=id).update(updatetime=str(datetime.datetime.now()))
            update_shop_products(shopname, userid)
            return JsonResponse({'msg': "It works!"})
    else:
        return JsonResponse({'msg': "It fails!"})


def product(request):
    userid = request.COOKIES.get('username', '')
    if userid:
        return render(request, 'product.html')


def kwproduct(request):
    userid = request.COOKIES.get('username', '')
    if userid:
        return render(request, 'kwproduct.html')


def keywords(request):
    userid = request.COOKIES.get('username', '')
    return render(request, 'keywords.html')


def show_product(request):
    uid = request.COOKIES.get('username', '')
    data_list = list()
    shopname = request.GET['name']
    temp_data = list(Products.objects.filter(uid__exact=uid, userid__exact=shopname, status__exact=0).order_by('-quantitysold').values())
    for detail in temp_data:
        detail['galleryurl'] = "<img src='" + detail['galleryurl'] + "' width='80' height='80'>"
        detail['title'] = "<a href='http://www.ebay.com/itm/" + detail['itemid'] + "' target='_Blank'>" + detail['title'] + "</a>"
        detail['starttime'] = str(detail['starttime'])[:10]
        detail['curdate'] = str(detail['curdate'])[:10]
        data_list.append(detail)

    response_data = json.dumps(data_list)
    return HttpResponse(response_data, content_type='application/json; charset=utf8')

def delete_product(request):
    uid = request.COOKIES.get('username', '')
    if request.method == "POST":
        if uid:
            id = request.POST.get('id')
            Products.objects.filter(id=id).delete()
            return JsonResponse({'msg': "It works!"})
    else:return JsonResponse({'msg': "It fails!"})


def remove_all_product(request):
    if request.method == "POST":
        userid = request.COOKIES.get('username', '')
        if userid:
            ids_string = request.POST.get('ids')
            ids_dict = json.loads(ids_string)
            ids = ids_dict['ids']
            for id in ids:
                 Products.objects.filter(id=id).delete()
            return JsonResponse({"msg":"it works!"})
        else:
            return JsonResponse({"msg":'it fails!'})


def  likeall_product(request):
    uid = request.COOKIES.get('username', '')
    if request.method == "POST":
        if uid:
            ids_string = request.POST.get('ids')
            ids_dict = json.loads(ids_string)
            ids = ids_dict['ids']
            for id in ids:
                Products.objects.filter(id=id).update(status=1)
            return JsonResponse({'msg': "It works!"})
    else: return JsonResponse({'msg': "It fails!"})


def like_product(request):
    uid = request.COOKIES.get('username', '')
    if request.method == "POST":
        if uid:
            id = request.POST.get('id')
            Products.objects.filter(id=id).update(status=1)
            return JsonResponse({'msg': "It works!"})
    else: return JsonResponse({'msg': "It fails!"})


def remove_all_kwproduct(request):
    if request.method == "POST":
        userid = request.COOKIES.get('username', '')
        if userid:
            ids_string = request.POST.get('ids')
            ids_dict = json.loads(ids_string)
            ids = ids_dict['ids']
            for id in ids:
                KWProducts.objects.filter(id=id).delete()
            return JsonResponse({"msg":"it works!"})
        else:
            return JsonResponse({"msg":'it fails!'})


def delete_kw_product(request):
    uid = request.COOKIES.get('username', '')
    if request.method == "POST":
        if uid:
            id = request.POST.get('id')
            KWProducts.objects.filter(id=id).delete()
            return JsonResponse({'msg': "It works!"})
    else:return JsonResponse({'msg': "It fails!"})


def likeall_kw_product(request):
    uid = request.COOKIES.get('username', '')
    if request.method == "POST":
        if uid:
            ids_string = request.POST.get('ids')
            ids_dict = json.loads(ids_string)
            ids = ids_dict['ids']
            for id in ids:
                KWProducts.objects.filter(id=id).update(status=1)
            return JsonResponse({'msg': "It works!"})
    else: return JsonResponse({'msg': "It fails!"})


def like_kw_product(request):
    uid = request.COOKIES.get('username', '')
    if request.method == "POST":
        if uid:
            id = request.POST.get('id')
            KWProducts.objects.filter(id=id).update(status=1)
            return JsonResponse({'msg': "It works!"})
    else: return JsonResponse({'msg': "It fails!"})

def like(request):
    return render(request, 'like.html')


def product_liked(request):
    uid = request.COOKIES.get('username', '')
    data_list = list()
    temp_shop = list(Products.objects.filter(uid__exact=uid, status__exact=1).order_by('-quantitysold').values())
    temp_kw = list(KWProducts.objects.filter(uid__exact=uid, status__exact=1).order_by('-quantitysold').values())
    temp_data = temp_kw + temp_shop
    for detail in temp_data:
        detail['galleryurl'] = "<img src='" + detail['galleryurl'] + "' width='80' height='80'>"
        detail['title'] = "<a href='http://www.ebay.com/itm/" + detail['itemid'] + "' target='_Blank'>" + detail['title'] + "</a>"
        detail['starttime'] = str(detail['starttime'])[:10]
        detail['curdate'] = str(detail['curdate'])[:10]
        data_list.append(detail)

    response_data = json.dumps(data_list)
    return HttpResponse(response_data, content_type='application/json; charset=utf8')


def editsku(request):
    uid = request.COOKIES.get('username', '')
    if request.method == "POST":
        if uid:
            id = request.POST.get('id')
            itemid = request.POST.get('itemid')
            sku = request.POST.get('mysku')
            if Products.objects.filter(id=id, itemid__exact=itemid):
                Products.objects.filter(id=id).update(mysku=sku)
            else:
                KWProducts.objects.filter(id=id).update(mysku=sku)
            return JsonResponse({id:sku})
    else:
        return JsonResponse({'msg': "It fails!"})


def get_keywords(request):
    uid = request.COOKIES.get('username', '')
    # id = request.GET.get('id')
    if uid:
        return JsonResponse(dict(data=list(KeyWords.objects.filter(userid__exact=uid).order_by('-id').values())))



def add_keywords(request):
    uid = request.COOKIES.get('username', '')
    if request.method == "POST":
        if uid:
            keywords = request.POST.get('keywords')
            curdate = str(datetime.datetime.now())
            KeyWords.objects.create(keywords=keywords, userid=uid, curdate=curdate)
            return JsonResponse({"msg": "it works!"})
    else:
        curdate = str(datetime.datetime.now())
        KeyWords.objects.create(keywords='fefefef', userid=uid, curdate=curdate)
        return JsonResponse({"msg": "testing!"})

def addallkw(request):
    if request.method == 'POST':
        userid = request.COOKIES.get('username', '')
        if userid:
            data2upload = request.POST.get('data')
            data_json = json.loads(data2upload)
            data = data_json['data']
            curdate = str(datetime.datetime.now())
            if data:
                for row in data:
                    keywords= row['keywords']     
                    KeyWords.objects.create(keywords=keywords, userid=userid, curdate=curdate)
                return JsonResponse({'msg':'it works!', 'code':0})
            else:
                return JsonResponse({"msg":"no content", 'code': 2})

    else:
        return JsonResponse({'msg':'no loggin!', 'code':1})

def remove_all_kw(request):
     if request.method == "POST":
        userid = request.COOKIES.get('username', '')
        if userid:
            ids_string = request.POST.get('ids')
            ids_dict = json.loads(ids_string)
            ids = ids_dict['ids']
            for id in ids:
                KeyWords.objects.filter(id=id).delete()
            return JsonResponse({"msg":"it works!"})
        else:
            return JsonResponse({"msg":'it fails!'})

def delete_keywords(request):
    uid = request.COOKIES.get('username', '')
    if request.method == "POST":
        if uid:
            id = request.POST.get('id')
            KeyWords.objects.filter(id=id).delete()
            return JsonResponse({'msg': "It works!"})
    else:return JsonResponse({'msg': "It fails!"})


def edit_keywords(request):
    if request.method == "POST":
        userid = request.COOKIES.get('username', '')
        if userid:
            id = request.POST.get('id')
            kw= request.POST.get('kw')
            KeyWords.objects.filter(id=id).update(keywords=kw)
            print "updating...."
            return JsonResponse({'msg': 'It works!'})

    else:
        return JsonResponse({'msg': 'It fails'})


def sync_keywords(request):
    if request.method == "POST":
        userid = request.COOKIES.get('username', '')
        if userid:
            keywords = request.POST.get('keywords')
            id = request.POST.get('id')
            KeyWords.objects.filter(id=id).update(updatetime=str(datetime.datetime.now()))
            update_keywords_product(keywords, userid)
            return JsonResponse({'msg': "It works!"})
    else:
        return JsonResponse({'msg': "It fails!"})


def show_kw_product(request):
    uid = request.COOKIES.get('username', '')
    data_list = list()
    # if request.method == "POST":
    key_words = request.GET['kw']
    print key_words
    print "I am here!"
    temp_data = list(KWProducts.objects.filter(uid__exact=uid, keywords__exact=key_words, status__exact=0).order_by('-quantitysold').values())
    for detail in temp_data:
        detail['galleryurl'] = "<img src='" + detail['galleryurl'] + "' width='80' height='80'>"
        detail['title'] = "<a href='http://www.ebay.com/itm/" + detail['itemid'] + "' target='_Blank'>" + detail['title'] + "</a>"
        detail['starttime'] = str(detail['starttime'])[:10]
        detail['curdate'] = str(detail['curdate'])[:10]
        data_list.append(detail)

    response_data = json.dumps(data_list)
    return HttpResponse(response_data, content_type='application/json; charset=utf8')


def watch_kw_shop(request):
    uid = request.COOKIES.get('username', '')
    if request.method == "POST":
        id = request.POST.get('id')
        data = KWProducts.objects.filter(id=id).values()
        if data:
            shop_data = list(data)[0]
            if Shops.objects.filter(shopname__exact=shop_data['userid']):
                Shops.objects.filter(shopname__exact=shop_data['userid']).update(
                    feedbackscore=shop_data['feedbackscore'],
                    curdate=str(datetime.datetime.now()))
            else:
                Shops.objects.create(shopname=shop_data['userid'], userid=uid, feedbackscore=shop_data['feedbackscore'],
                                     curdate=str(datetime.datetime.now()))
        return JsonResponse({'msg': 'it works!'})


def remove_liked(request):
    uid = request.COOKIES.get('username', '')
    if request.method == "POST":
        if uid:
            id = request.POST.get('id')
            itemid = request.POST.get('itemid')
            if Products.objects.filter(id=id, itemid__exact=itemid):
                Products.objects.filter(id=id).delete()
            else:
                KWProducts.objects.filter(id=id, itemid__exact=itemid).delete()
        return JsonResponse({'msg': 'it works!'})
    else:
        return JsonResponse({'mgs': 'please post!'})