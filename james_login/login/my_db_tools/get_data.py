#! usr/bin/env/python
# -*-coding:utf8-*-

import MySQLdb

def get_recom(uid):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='urnothing', db='django_user')
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    sql = [
            "select currentprice,title,starttime,galleryurl,id,currency,itemid,datediff(curdate,starttime) as deltaday, (quantitysold+0)/datediff(now(),starttime)  as avgsold,'products' as tablename",
            " from login_products where (quantitysold+0)/datediff(now(),starttime)>=0.5 and status=0 and uid='" + uid +"'",
            "union",
           "select currentprice,title,starttime,galleryurl,id,currency,itemid,datediff(curdate,starttime) as deltaday, (quantitysold+0)/datediff(now(),starttime)  as avgsold,'kwproducts' as tablename",
            " from login_kwproducts where (quantitysold+0)/datediff(now(),starttime)>=0.5 and status=0 and uid='" + uid + "'",
           
            ]
    query = ' '.join(sql)
    print query
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



if __name__ == "__main__":
    print get_recom('james').next()
