
from ebaysdk.finding import Connection
from multiprocessing import Pool
from functools import partial
from datetime import date, datetime


def find_advanced(page, key_words):
    "get the 100*100 listings in Category 20349 and limited using keywords"
    # proxies = {}
    item_list = list()
    api = Connection(
        # domain='api.ebay.com',
        timeout=6,
        appid='ZhouPeng-3242-4cc7-88fd-310f513fcd71',
        devid='df3f2898-65b1-4e15-afd5-172b989903aa',
        certid='a0e19cf9-9b2b-457f-b6f1-87f3f600ca63',
        token='AgAAAA**AQAAAA**aAAAAA**cJyLVQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wMkoqiC5mHoQmdj6x9nY+seQ**N+QCAA**AAMAAA**nLCwNt4AQt1TRtd2ydNIMuZ2JYnQZKVVYarn41QQfBSqccEDld22ltKr+C/HJTN8AKD4+jn/nIEqtjNMkmh9sxTIa6jVVLAH5sN/93X7gTCmTkOsE/Av612U90nRoyQJ5bX1+NO25tMDZs9U0aTJIwVVu1BAB8/nsjL0pTCWw7KZACJ+a/aQ6swXLvSvOCWIBjFyCaWibKZseT2LoJMvJQmC2QpIuDsQ8cTYozLUYZqC88uKAjo7DNWIvaPVCdwkp/Vux3arR1Asin4ewX1l+LWCamWsXeBiVyaYq/oEUXABgknieVAPEpaFAfSzlrcTNmTWLBDDRwRGI/8hJCwK6/eJWexGrLk7U7p0kRltktNseTckAKT7g1ED4C5gUeQ4/nTHsNQBejUPTzTlwBWTJpwRaBFD7dAlbagH+TKaEJK41Esf/ZpL2599LUMolsO8tBgo0BhtCF/bYtdUUfopksIKNUwPXikadUxx6TurknnTtR1WDD229uUJIIf9BCS68WB56OfDTdXcZ8rdPZ0zdHuw5+BRxrumpFUzTQb5fJeHRDLPtQbLdX5rFPrS+NPJl6Qzi7bWNxUCydNQcIzKv7xLquIPoPx8bD1PRCoQbzjTQsOqhe9PBvLtcJ0Ggve78YjQKb5nDt6YThZ6D+1EOKdcthU03VizDfBKBLJ/NPqktDTx74tsS3l4feAjblGDoQ2RZXefJ9Jk3t+Qc4khlvl4mKpjZ4sCakh4qPWr9H6t3CN80hz5MO1Y7uHPUY61',
        config_file=None, 
        #proxy_host='127.0.0.1', 
        #proxy_port='1080'
        )
    input_para = {
        # 'categoryId': category_id,
        'keywords': key_words,
        'sortOrder': 'BestMatch',
        'outputSelector': 'SellerInfo',
        'paginationInput': {'pageNumber': 0},
        'itemFilter': [
            {'name': 'ListingType', 'value': 'FixedPrice'},
            {'name': 'AvailableTo', 'value': 'US'}
        ]
    }
    input_para['paginationInput']['pageNumber'] = page

    # print response.reply
    try:
        response = api.execute('findItemsAdvanced', input_para)
        items = response.reply.searchResult.item
        for item in items:
            # input_single(item.itemId,item.listingInfo.startTime,key_words,owner)
            id = item.itemId
            start_time = item.listingInfo.startTime
            today = datetime2date(datetime.now())
            start_date = datetime2date(start_time)
            delta_days = (today-start_date).days
            # print id, delta_days, start_time
            if delta_days <= 30:
                item_list.append(id)
        obj_list = list(set(item_list))
        # print obj_list
        return obj_list
    except Exception as e:
        print e


def datetime2date(time):
    time_split = str(time)[:10].split('-')
    return date(int(time_split[0]), int(time_split[1]), int(time_split[2]))


def get_category_list(keywords):
    p = Pool(4)
    test_set = p.map(partial(find_advanced, key_words=keywords), range(1, 50))
    sum_list = []
    if test_set:
        for item in test_set:
            if item:
                sum_list = sum_list + item
            # print sum_list
    p.close()
    p.join()
    return list(set(sum_list))


if __name__ == "__main__":
    # for i in range(1, 50):
    #     for item in find_advanced("iphone 7 case", i):
    #         print item
    print get_category_list('christmas flag')
    # print datetime2date('2016-05-21 00:25:23')