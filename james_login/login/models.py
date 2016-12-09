from __future__ import unicode_literals

from django.db import models

import datetime
# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __unicode__(self):
        return self.username


class Shops(models.Model):
    shopname = models.CharField(max_length=50)
    userid = models.CharField(max_length=20)
    curdate = models.DateTimeField()
    feedbackscore = models.IntegerField()
    updatetime = models.DateTimeField(null=True)
    def __unicode__(self):
        return self.shopname

class KeyWords(models.Model):
    keywords = models.CharField(max_length=100)
    userid = models.CharField(max_length=20)
    curdate = models.DateTimeField()
    updatetime = models.DateTimeField(null=True)
    def __unicode__(self):
        return self.keywords


class Products(models.Model):
    country = models.CharField(max_length=30)
    currency = models.CharField(max_length=5)
    hitcounter = models.CharField(max_length=20)
    itemid = models.CharField(max_length=20)
    starttime = models.DateTimeField(null=True)
    viewitemurl = models.CharField(max_length=250)
    location = models.CharField(max_length=20)
    categoryid = models.CharField(max_length=8)
    feedbackscore = models.CharField(max_length=9)
    usersite = models.CharField(max_length=20)
    userid = models.CharField(max_length=40)
    storeowner = models.CharField(max_length=6)
    currentprice = models.CharField(max_length=7)
    quantitysold = models.IntegerField()
    quantitysoldinstore = models.CharField(max_length=4)
    shippingservice = models.CharField(max_length=50)
    shippingcost = models.CharField(max_length=5)
    title = models.CharField(max_length=200)
    hitcount = models.CharField(max_length=12)
    sku = models.CharField(max_length=13)
    galleryurl = models.CharField(max_length=250)
    listduration = models.CharField(max_length=20)
    privatelisting = models.CharField(max_length=5)
    curdate = models.DateTimeField(null=True)
    deltatitle = models.CharField(max_length=5)
    deltasold = models.CharField(max_length=6)
    deltahit = models.CharField(max_length=6)
    deltaprice = models.CharField(max_length=6)
    listingstatus = models.CharField(max_length=20)
    deltadays = models.IntegerField()
    uid = models.CharField(max_length=50)
    status = models.CharField(max_length=2,default=0)
    mysku = models.CharField(max_length=20, null=True,blank=True)
    def __unicode__(self):
        return self.itemid


class KWProducts(models.Model):
    country = models.CharField(max_length=30)
    currency = models.CharField(max_length=5)
    hitcounter = models.CharField(max_length=20)
    itemid = models.CharField(max_length=20)
    starttime = models.DateTimeField(null=True)
    viewitemurl = models.CharField(max_length=250)
    location = models.CharField(max_length=20)
    categoryid = models.CharField(max_length=8)
    feedbackscore = models.CharField(max_length=9)
    usersite = models.CharField(max_length=20)
    userid = models.CharField(max_length=40)
    storeowner = models.CharField(max_length=6)
    currentprice = models.CharField(max_length=7)
    quantitysold = models.IntegerField()
    quantitysoldinstore = models.CharField(max_length=4)
    shippingservice = models.CharField(max_length=50)
    shippingcost = models.CharField(max_length=5)
    title = models.CharField(max_length=200)
    hitcount = models.CharField(max_length=12)
    sku = models.CharField(max_length=13)
    galleryurl = models.CharField(max_length=250)
    listduration = models.CharField(max_length=20)
    privatelisting = models.CharField(max_length=5)
    curdate = models.DateTimeField(null=True)
    deltatitle = models.CharField(max_length=5)
    deltasold = models.CharField(max_length=6)
    deltahit = models.CharField(max_length=6)
    deltaprice = models.CharField(max_length=6)
    listingstatus = models.CharField(max_length=20)
    deltadays = models.IntegerField()
    uid = models.CharField(max_length=50)
    status = models.CharField(max_length=2,default=0)
    mysku = models.CharField(max_length=2,null=True,blank=True)
    keywords = models.CharField(max_length=50, null=True,blank=True)
    def __unicode__(self):
        return self.itemid
