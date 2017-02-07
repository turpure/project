import MySQLdb

def get_items_to_update():
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='urnothing', db='django_user')
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    sql = [
    "select itemid,quantitysold,hitcount,curdate,'login_kwproducts' as tablename from login_kwproducts where datediff(now(),curdate)>=7 and status!='10'  ",
    "union",
    "select itemid,quantitysold,hitcount,curdate,'login_products' as tablename from login_products where datediff(now(),curdate)>=7 and status!='10' "
    ]
    query = ' '.join(sql)
    print query
    try:
        cur.execute(query)
        ret = cur.fetchall()
        for row in ret:
            yield row
    except:
        yield None
    finally:
        con.close()

if __name__ == '__main__':
    print get_items_to_update().next()


