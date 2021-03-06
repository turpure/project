#! usr/bin/env/python
# -*-coding:utf8-*-

import MySQLdb
def get_recom(uid):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='urnothing', db='django_user')
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    sql = [
            "select max((currentprice + shippingcost)) as currentprice ,max(title) as title,max(starttime) as starttime,max(galleryurl) as galleryurl ,max(id) as id,max(currency) as currency,max(itemid) as itemid ,max(datediff(curdate,starttime)) as deltaday, max((quantitysold+0)/datediff(now(),starttime))  as avgsold,'products' as tablename",
            " from login_products where (quantitysold+0)/datediff(now(),starttime)>=0.5 and status=0 and uid='" + uid +"' group by itemid",
            "union",
           "select max((currentprice + shippingcost)) as currentprice ,max(title) as title,max(starttime) as starttime,max(galleryurl) as galleryurl ,max(id) as id,max(currency) as currency,max(itemid) as itemid ,max(datediff(curdate,starttime)) as deltaday, max((quantitysold+0)/datediff(now(),starttime))  as avgsold,'products' as tablename",
            " from login_kwproducts where (quantitysold+0)/datediff(now(),starttime)>=0.5 and status=0 and uid='" + uid + "' group by itemid",
           
            ]
    query = ' '.join(sql)
    try:
        cur.execute(query)
        products = cur.fetchall()
        for row in products:
            row['starttime'] = str(row['starttime'])[:10]
            row['galleryurl'] = ' '.join([
                "<img src='",
                row['galleryurl'],
                "' width='100' height='80'>"
                ])
            row['title'] = "".join([
            "<a href='http://www.ebay.com/itm/",
            row['itemid'],
            "' target='_Blank'>",
            row['title'],
            "</a>"
            ])
            yield row
    except Exception as e:
        print e
    finally:
        con.close()


def get_newly_products(uid):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='urnothing', db='django_user')
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    sql = [
            "select  max((currentprice + shippingcost)) as currentprice ,max(title) as title,max(starttime) as starttime,max(galleryurl) as galleryurl ,max(id) as id,max(currency) as currency ,max(itemid) as itemid , max(datediff(curdate,starttime)) as deltaday, max((quantitysold+0)/datediff(now(),starttime))  as avgsold,'products' as tablename",
            " from login_products where  datediff(now(),starttime)=1 and status=0 and uid='" + uid +"'group by itemid" ,
            "union",
           "select  max((currentprice + shippingcost)) as currentprice ,max(title) as title,max(starttime) as starttime,max(galleryurl) as galleryurl ,max(id) as id,max(currency) as currency ,max(itemid) as itemid , max(datediff(curdate,starttime)) as deltaday, max((quantitysold+0)/datediff(now(),starttime))  as avgsold,'products' as tablename",
            " from login_kwproducts where  datediff(now(),starttime)=1  and status=0 and uid='" + uid + "'group by itemid",
            ]
    query = ' '.join(sql)
    try:
        cur.execute(query)
        products = cur.fetchall()
        for row in products:
            row['starttime'] = str(row['starttime'])[:10]
            row['galleryurl'] = ' '.join([
                "<img src='",
                row['galleryurl'],
                "' width='100' height='80'>"
                ])
            row['title'] = "".join([
            "<a href='http://www.ebay.com/itm/",
            row['itemid'],
            "' target='_Blank'>",
            row['title'],
            "</a>"
            ])
            yield row
    except Exception as e:
        yield None
    finally:
        con.close()

def get_hot_products(uid):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='urnothing', db='django_user')
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    sql = [
            "select max((currentprice + shippingcost)) as currentprice ,max(title) as title, max(starttime) as starttime,max(galleryurl) as galleryurl,max(id) as id,max(currency) as currency,max(itemid) as itemid,max(deltadays) as deltadays, max(deltasold) as deltasold ,max(deltahit) as deltahit ,'products' as tablename",
            " from login_products where  deltasold>0 and deltadays>=7 and status=0 and uid='" + uid +"' group by itemid",
            "union",
           "select max((currentprice + shippingcost)) as currentprice ,max(title) as title, max(starttime) as starttime,max(galleryurl) as galleryurl,max(id) as id,max(currency) as currency,max(itemid) as itemid,max(deltadays) as deltadays, max(deltasold) as deltasold ,max(deltahit) as deltahit ,'products' as tablename",
            " from login_kwproducts where deltasold>0 and deltadays>=7  and status=0 and uid='" + uid + "' group by itemid",
            ]
    query = ' '.join(sql)
    try:
        cur.execute(query)
        products = cur.fetchall()
        for row in products:
            row['starttime'] = str(row['starttime'])[:10]
            row['galleryurl'] = ' '.join([
                "<img src='",
                row['galleryurl'],
                "' width='100' height='80'>"
                ])
            row['title'] = "".join([
            "<a href='http://www.ebay.com/itm/",
            row['itemid'],
            "' target='_Blank'>",
            row['title'],
            "</a>"
            ])
            yield row
    except Exception as e:
        yield None
    finally:
        con.close()


def get_shops_to_update():
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='urnothing', db='django_user')
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    sql = [
    "select shopname,userid as uid, ",
    "if(DATEDIFF(now(),IFNULL(updatetime,DATE_ADD(now(),INTERVAL -1 day)))>10,10,DATEDIFF(now(),IFNULL(updatetime,DATE_ADD(now(),INTERVAL -1 day)))) ",
    "as deltaday",
    "from login_shops where shopname != '' "
    ]
    updatetime_sql = "update login_shops set updatetime=now()"
    try:
        query = ' '.join(sql)
        cur.execute(query)
        ret = cur.fetchall()
        cur.execute(updatetime_sql)
        con.commit()
        for row in ret:
            yield row 
    except:
        yield None
    finally:
        con.close()


def get_keywords_to_update():
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='urnothing', db='django_user')
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    sql = "select userid as uid,keywords from login_keywords where IFNULL(keywords,'')!=''"
    updatetime_sql = "update login_keywords set updatetime=now()"
    try:
        cur.execute(sql)
        ret = cur.fetchall()
        cur.execute(updatetime_sql)
        con.commit()
        for row in ret:
            yield row
    except:
        yield None
    finally:
        con.close()

if __name__ == "__main__":
    #print get_recom('james').next()
    for row in get_hot_products('james'):
        print row
        
