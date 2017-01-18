
from ebaysdk.finding import Connection
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 
from functools import partial
from datetime import date, datetime

def find_advanced(page, key_words):
    "get the 100*100 listings in Category 20349 and limited using keywords"
    # proxies = {}
    item_list = list()
    api = Connection(
        # domain='api.ebay.com',
        timeout=10,
        appid='ZhouPeng-3242-4cc7-88fd-310f513fcd71',
        devid='df3f2898-65b1-4e15-afd5-172b989903aa',
        certid='a0e19cf9-9b2b-457f-b6f1-87f3f600ca63',
        # token='AgAAAA**AQAAAA**aAAAAA**cJyLVQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wMkoqiC5mHoQmdj6x9nY+seQ**N+QCAA**AAMAAA**nLCwNt4AQt1TRtd2ydNIMuZ2JYnQZKVVYarn41QQfBSqccEDld22ltKr+C/HJTN8AKD4+jn/nIEqtjNMkmh9sxTIa6jVVLAH5sN/93X7gTCmTkOsE/Av612U90nRoyQJ5bX1+NO25tMDZs9U0aTJIwVVu1BAB8/nsjL0pTCWw7KZACJ+a/aQ6swXLvSvOCWIBjFyCaWibKZseT2LoJMvJQmC2QpIuDsQ8cTYozLUYZqC88uKAjo7DNWIvaPVCdwkp/Vux3arR1Asin4ewX1l+LWCamWsXeBiVyaYq/oEUXABgknieVAPEpaFAfSzlrcTNmTWLBDDRwRGI/8hJCwK6/eJWexGrLk7U7p0kRltktNseTckAKT7g1ED4C5gUeQ4/nTHsNQBejUPTzTlwBWTJpwRaBFD7dAlbagH+TKaEJK41Esf/ZpL2599LUMolsO8tBgo0BhtCF/bYtdUUfopksIKNUwPXikadUxx6TurknnTtR1WDD229uUJIIf9BCS68WB56OfDTdXcZ8rdPZ0zdHuw5+BRxrumpFUzTQb5fJeHRDLPtQbLdX5rFPrS+NPJl6Qzi7bWNxUCydNQcIzKv7xLquIPoPx8bD1PRCoQbzjTQsOqhe9PBvLtcJ0Ggve78YjQKb5nDt6YThZ6D+1EOKdcthU03VizDfBKBLJ/NPqktDTx74tsS3l4feAjblGDoQ2RZXefJ9Jk3t+Qc4khlvl4mKpjZ4sCakh4qPWr9H6t3CN80hz5MO1Y7uHPUY61',
        token = 'AgAAAA**AQAAAA**aAAAAA**aCRbWA**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wDmYShCJCHogmdj6x9nY+seQ**N+QCAA**AAMAAA**ktFg8zDYputToOiGDvTfZku93pjbVq3rGn7AR53h1eWAByiTLP+Gd8uKuDof0BQ0prvskMARI/nHxkjFYUp7IUsQkZ6sH/E2UmmvRRwqDHZ/XsXt0+meLqS6ZHMjw7v/CpISJqnZjGChDSYPFRe6RboawkjPi8ial5wEXojlvNWvHl02yT92ih6dTYj44g2xprmmyOSyTYC8l8oG+YLKZ+FPzOj5zxO3Qm8rhVtQwc1KGGtHnthz2ZwHwbeFDh8cVp1qaFQmCaHc27ftM8/to2U22mccon5zRk6yf59EiN88WPzag/ii0XpkwELXWRsHKBfl/9pepWUqWZvgjhQ9jcGQsrYyQfS6T54dLcaJ7a2IrCxOvpdkv4Z26T7CpTpUBbYzG4olJI42jFMZBu5quqOanio2qbHNFov5Jq85jMR9Zx51KlKezNaauIW16upj7P2gvCwDt+E7xCQMoqKDrIyx7J0g0KLHKhSavzeC0vnrF0H9NAfqxVEdYtLUgbR9A8JQagPAYp+vPuMpSEbhc5/fTLBfD6YFSoJ+izMzx0n6Gj2df5n77hS3X1850eLzqzCREtUClZfJ7tcTMR+oU8i0aB75rWDr/sFKsfgW/rAe8hcuMzYBms+rsL4i7ddt5KWfCieMksAfabdUrPF5Owfr/24en/omwHXtBrb39u/oMKTfGZOS2JKyXdbpmpV1YWsJ8eDzxNIN0hJfG6wqrjdEJAUX5dkg4j5L5UXE6deogb9MUYHJgkP3nch5yPfS',
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

    flag = 3
    
    while  flag>0:
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
                if delta_days <= 60:
                    item_list.append(id)
            obj_list = list(set(item_list))
            # print obj_list
            return obj_list
        except IOError as e:
            print '%s:%s' % ('find_advanced', e)
            flag -=1
        except AttributeError as e:
            print '%s:%s' % ('find_advanced', e)



def datetime2date(time):
    time_split = str(time)[:10].split('-')
    return date(int(time_split[0]), int(time_split[1]), int(time_split[2]))

# multi process
# def get_category_list(keywords):
#     p = Pool(4)
#     test_set = p.map(partial(find_advanced, key_words=keywords), range(1, 50))
#     sum_list = []
#     if test_set:
#         for item in test_set:
#             if item:
#                 sum_list = sum_list + item
#             # print sum_list
#     p.close()
#     p.join()
#     return list(set(sum_list))

#multi threading
def get_category_list(keywords):
    p = ThreadPool(8)
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


# single process
# def get_category_list(keywords):
#     for page in range(1,50):
#         ret = find_advanced(page,keywords)
#         yield ret
  


if __name__ == "__main__":
    # for i in range(20):
        # find_advanced(i,'christmas flag')
    for data in get_category_list('christmas flag'):
        print data
    