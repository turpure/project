
from twisteditem import GetFiledsByItemid
import datetime
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 
from ebaydate import monthrange
from getlist import GetList
import MySQLdb
from functools import partial
from FindByCategory import get_category_list


def insert_data(detail, uid):
    now = datetime.datetime.now()
    check = 'select id from login_products where itemid=%s'
    query = ''.join([
        'insert into login_products',
        '(',
        'country,currency,hitcounter,itemid,',
        'viewitemurl,location,categoryid,',
        'feedbackscore,usersite,userid,storeowner,',
        'currentprice, quantitysold, quantitysoldinstore,',
        'shippingservice,shippingcost, title, hitcount,sku,',
        'galleryurl,listduration, privatelisting,deltatitle,',
        'deltasold,deltahit, deltaprice, listingstatus,deltadays,starttime,uid,curdate,status,mysku',
        ')',
        ' values',
        '(',
        '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,',
        '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,',
        '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s',
        ')',
    ])
    try:
        con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='urnothing', db='django_user')
        cur = con.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(check, (detail['itemid'],))
        result = cur.fetchone()
        if not result:
            cur.execute(query, (detail['country'], detail['currency'],
                                detail['hitcounter'], detail['itemid'],
                                detail['viewitemurl'], detail['location'],
                                detail['categoryid'], detail['feedbackscore'],
                                detail['usersite'], detail['userid'],
                                detail['storeowner'], detail['currentprice'],
                                detail['quantitysold'], detail['quantitysoldinstore'],
                                detail['shippingservice'], detail['shippingcost'],
                                detail['title'], detail['hitcount'], detail['sku'],
                                detail['galleryurl'], detail['listduration'],
                                detail['privatelisting'], 0, 0, 0, 0,
                                detail['listingstatus'], 0, detail['starttime'], uid, now, 0,''
                                ))
            print 'puting: %s' % detail['itemid']
            con.commit()
    except Exception as e:
        print e
    con.close()


def insert_kw_data(detail, uid, keywords):
    now = datetime.datetime.now()
    check = 'select id from login_kwproducts where itemid=%s'
    query = ''.join([
        'insert into login_kwproducts',
        '(',
        'country,currency,hitcounter,itemid,',
        'viewitemurl,location,categoryid,',
        'feedbackscore,usersite,userid,storeowner,',
        'currentprice, quantitysold, quantitysoldinstore,',
        'shippingservice,shippingcost, title, hitcount,sku,',
        'galleryurl,listduration, privatelisting,deltatitle,',
        'deltasold,deltahit, deltaprice, listingstatus,deltadays,starttime,uid,curdate,status,mysku,keywords',
        ')',
        ' values',
        '(',
        '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,',
        '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,',
        '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s',
        ')',
    ])
    try:
        con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='urnothing', db='django_user')
        cur = con.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(check, (detail['itemid'],))
        result = cur.fetchone()
        if not result:
            cur.execute(query, (detail['country'], detail['currency'],
                                detail['hitcounter'], detail['itemid'],
                                detail['viewitemurl'], detail['location'],
                                detail['categoryid'], detail['feedbackscore'],
                                detail['usersite'], detail['userid'],
                                detail['storeowner'], detail['currentprice'],
                                detail['quantitysold'], detail['quantitysoldinstore'],
                                detail['shippingservice'], detail['shippingcost'],
                                detail['title'], detail['hitcount'], detail['sku'],
                                detail['galleryurl'], detail['listduration'],
                                detail['privatelisting'], 0, 0, 0, 0,
                                detail['listingstatus'], 0, detail['starttime'], uid, now, 0,'' ,keywords
                                ))
            print 'puting: %s' % detail['itemid']
            con.commit()
    except Exception as e:
        print '%s:%s' % ('insert_kw_data', e)
    con.close()

def get_item_list(shop_name):
    my_list = GetList()
    for per in monthrange(1, 2):
        arg = (shop_name, per[0]+'T15:02:52.000Z', per[1]+'T15:02:52.000Z')
        items = my_list.get_list(arg[0], arg[1], arg[2])
        if items:
            for item in items:
                if item:
                    yield item


def handle(id, uid):
        my_item = GetFiledsByItemid()
        xml = my_item.get_xml(id)
        if xml:
            detail = my_item.parse(xml)
            # detail['listduration'] == u'GTC' and
            if  int(detail['quantitysold']) != 0:
                # print detail
                insert_data(detail, uid)
                # return detail


def handle_kw(id, uid, keywords):
    my_item = GetFiledsByItemid()
    xml = my_item.get_xml(id)
    if xml:
        detail = my_item.parse(xml)
        # detail['listduration'] == u'GTC' and
        if int(detail['quantitysold']) > 0:
            # print detail
            insert_kw_data(detail, uid, keywords)


def update_shop_products(shopname, uid):
    p = ThreadPool(4)
    try:
        p.map(partial(handle, uid=uid),  get_item_list(shopname))
    except Exception as e:
        print e
    p.close()
    p.join()


def update_keywords_product(keywords, uid):
    p = ThreadPool(4)
    try:
        item_list = get_category_list(keywords)
        # print item_list
        p.map(partial(handle_kw, uid=uid, keywords=keywords), item_list)
    except Exception as e:
        print e
    p.close()
    p.join()



if __name__ =="__main__":
    # for itemid in get_item_list('7color7'):
    #     print itemid
    # item_list = ['112146443310']
    # detail = map(handle, item_list)
    # print detail
    update_keywords_product('men shoes', 'test')


