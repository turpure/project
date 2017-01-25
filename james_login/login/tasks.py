from __future__ import absolute_import
import time
from celery.task import task
from login.my_ebay_tools.myshop import update_shop_products, update_keywords_product
from login.my_db_tools.get_data import get_shops_to_update
import json
import requests
import MySQLdb

@task
def _do_kground_work(name):
	for i in range(1, 10):
		print 'hello : %s %s' % (name, i)
		time.sleep(1)

@task
def sync_shop_products(shopname,deltaday, uid):
	update_shop_products(shopname, deltaday,uid)

@task
def sync_keywords_product(keywords, uid):
	update_keywords_product(keywords, uid)

def add_task(task_name, args):
    base_url = 'http://192.168.199.136:5555/api/task/apply/login.tasks.%s' % task_name
    data = {
    'args':args
    }
    ret = requests.post(base_url, data=json.dumps(data))
    res = ret.json()
    return res

@task
def auto_update_shops():
    shops = get_shops_to_update()
    for row in shops:
        update_shop_products(row['shopname'],row['deltaday'],row['uid'])







