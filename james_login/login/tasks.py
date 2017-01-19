import time
from celery.task import task
from my_ebay_tools.myshop import update_shop_products, update_keywords_product
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