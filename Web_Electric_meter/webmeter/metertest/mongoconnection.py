# coding=UTF-8
"""
Version: 1
Creater: Hsu
Detail: No ood
"""
from pymongo import MongoClient
from datetime import datetime, date, time, timedelta
from metertest import my_time
import happybase
import  json
import bson
from bson.son import SON
def dumptoJson(devices, allDeviceist, timerange, Devicedict):
    timedumpnum = len(timerange) - 1
    if devices == allDeviceist:
        allkwh = []
        for i in range(timedumpnum):
            sum_kwh = 0
            for r in allDeviceist:
                sum_kwh += Devicedict[r][i]
            allkwh.append(sum_kwh)

        listcontent = []
        for i in range(len(allkwh)):
            mdict = {"Time":timerange[i].strftime("%Y-%m-%d %H:%M:%S")+':000',"Device_KWH":[{"ALL":allkwh[i]}]}
            listcontent.append(mdict)
        dictjson = {'Data':listcontent}
        return json.dumps(dictjson)
    else:
        listcontent = []
        for i in range(timedumpnum):
            mdict = {"Time":timerange[i].strftime("%Y-%m-%d %H:%M:%S")}
            listdevicekwh = []
            for row in devices:
                listdevicekwh.append({ row: Devicedict[row][i]})
            mdict['Device_KWH'] = listdevicekwh
            listcontent.append(mdict)
        dictjson = {'Data':listcontent}
        return json.dumps(dictjson)
def dumptoJsondj(devices, allDeviceist, timerange, Devicedict):
    timedumpnum = len(timerange) - 1
    if devices == allDeviceist:
        allkwh = []
        for i in range(timedumpnum):
            sum_kwh = 0
            for r in allDeviceist:
                sum_kwh += Devicedict[r][i]
            allkwh.append(sum_kwh)

        listcontent = []
        for i in range(len(allkwh)):
            mdict = {"Time":timerange[i].strftime("%Y-%m-%d %H:%M:%S")+':000',"Device_KWH":[{"ALL":allkwh[i]}]}
            listcontent.append(mdict)
        dictjson = {'Data':listcontent}
        return dictjson
    else:
        listcontent = []
        for i in range(timedumpnum):
            mdict = {"Time":timerange[i].strftime("%Y%m%d-%H:%M:%S")+':000'}
            listdevicekwh = []
            for row in devices:
                listdevicekwh.append({ row: Devicedict[row][i]})
            mdict['Device_KWH'] = listdevicekwh
            listcontent.append(mdict)
        dictjson = {'Data':listcontent}
        return dictjson
def Rangequery(devices, time1, time2, searchtype):
    client = MongoClient('localhost')
    db = client.test_webbase
    timerange = my_time.mytime(time1, time2, searchtype).calculatetime()
    x = db.collection_names()

    if devices == []:
        devices = db.collection_names()


    Devicedict = {}

    for device_id in devices:
        collection = db[device_id]
        print(collection)
        Timelist = []
        DeviceKwh_list = []
        for index in range(len(timerange) - 1):
            sum_kwh = 0
            # try:
            decidecount = collection.find({'Capaturetime':{'$gte':timerange[index],'$lt':timerange[index+1]}}).limit(20)
            if decidecount.count() == 0:
                try:
                    pool = happybase.ConnectionPool(size=3,host='localhost')
                    print("hbase in")
                    rowkeyvalue1 = timerange[index].strftime("%Y%m%d%H%M%S")
                    rowkeyvalue1+='000'
                    rowkeyvalue2 = timerange[index+1].strftime("%Y%m%d%H%M%S")
                    rowkeyvalue2 = rowkeyvalue2+'000'
                    with pool.connection() as connection:
                        table = connection.table(device_id)
                        count = 0
                        for key, data in table.scan(row_start = rowkeyvalue1,columns = [b'KWH:KWH'], row_stop = rowkeyvalue2):
                            bytedara = data[b'KWH:KWH']
                            decodevute = float(bytedara.decode("ascii"))
                            count+=1
                            sum_kwh += decodevute
                        print(count,sum_kwh)

                        DeviceKwh_list.append(sum_kwh)
                        Devicedict[device_id] = DeviceKwh_list
                except:
                    print("hbase fail")
                    DeviceKwh_list.append(0)
                    Devicedict[device_id] = DeviceKwh_list
            else:
                try:
                    print('here')
                    for post in b.collection.find({'Capaturetime':{'$gte':timerange[index],'$lt':timerange[index+1]}}):
                        sum_kwh += post['KWH']
                            # Timelist.append(timerange[index])
                    print(timerange[index],sum_kwh)
                    DeviceKwh_list.append(sum_kwh)
                    Devicedict[device_id] = DeviceKwh_list
                except:
                    DeviceKwh_list.append(0)
                    Devicedict[device_id] = DeviceKwh_list
    client.close()
    x = dumptoJsondj(devices,x,timerange,Devicedict)
    return x
    # for r in devices:\
"""
Version 2
if no all cache hbase
"""
def mongoaggregate(time1, time2, collection):
    match = {'Capaturetime': {'$gt': time1,'$lte': time2}}
    group1 = {'_id': None,'firsttime':{'$first':'$Capaturetime'},'firstkwh':{'$first':'$KWH'},'lastkwh':{'$last':'$KWH'},'lasttime':{'$last':'$Capaturetime'}}
    datacollect = collection.aggregate([{'$match': match},{'$group': group1}])
    datalist = list(datacollect)
    return datalist[0]
def Rangequeryv2(devices, time1, time2, searchtype):
    client = MongoClient('localhost')
    db = client.test_webbase
    timerange = my_time.mytime(time1, time2, searchtype).calculatetime()
    print(timerange)
    x = db.collection_names()
    if devices == []:
        devices = db.collection_names()
        print(devices)
    Devicedict = {}
    for device_id in devices:
        collection = db[device_id]
        booleanhbase = False
        DeviceKwh_list = []
        for index in range(len(timerange) - 1):
            mongoTime = timerange[index]
            sum_kwh = 0
            rowkeyvalue1 = timerange[index].strftime("%Y%m%d%H%M%S")
            rowkeyvalue1+='000'
            rowkeyvalue2 = timerange[index+1].strftime("%Y%m%d%H%M%S")
            rowkeyvalue2 = rowkeyvalue2+'000'
            try:
                print("mongo")
                datadict = mongoaggregate(timerange[index], timerange[index+1],collection)
                sum_kwh = abs(datadict['lastkwh'] - datadict['firstkwh'])
                if int(datadict['lasttime'].strftime("%Y%m%d%H%M%S")) < int(timerange[index+1].strftime("%Y%m%d%H%M%S")):
                    mongoTime = datadict['lasttime']
                    booleanhbase = True
            except:
                print("mongo fail")
                booleanhbase = True
            if booleanhbase:
                try:
                    pool = happybase.ConnectionPool(size=3,host='localhost')
                    rowkeyvalue1 = mongoTime.strftime("%Y%m%d%H%M%S")+'000'
                    print(rowkeyvalue1)
                    print(rowkeyvalue2)
                    kwh = 0.0
                    kwhlist = []
                    count = 0
                    initial = 0
                    last = 0
                    with pool.connection() as connection:
                        table = connection.table(device_id)
                        for key, data in table.scan(row_start = rowkeyvalue1,columns = [b'KWH:KWH'], row_stop = rowkeyvalue2):
                            bytedara = data[b'KWH:KWH']
                            decodevute = float(bytedara.decode("ascii"))
                            if count == 0:
                                print("here")
                                initial = decodevute
                                count+=1
                            last = decodevute
                        print(last)
                        sum_kwh += (last - initial)
                except:
                    print("hbase fail")
                booleanhbase = False
            DeviceKwh_list.append(sum_kwh)
            Devicedict[device_id] = DeviceKwh_list
    client.close()
    x = dumptoJsondj(devices,x,timerange,Devicedict)
    return x
    # for r in devices

# x = my_time.mytime('2017-01-01 2:10:00','2017-01-01 3:10:00',1)
# y = Rangequeryv2(['kdd91201'],'2016-1-1 0:00:00','2016-3-1 0:0:00',3)
# print(y)
def Rangequeryv3(devices, time1, time2, searchtype):
    client = MongoClient('localhost')
    db = client.test_webbase
    timerange = my_time.mytime(time1, time2, searchtype).calculatetime()
    x = db.collection_names()

    if devices == []:
        devices = db.collection_names()


    Devicedict = {}

    for device_id in devices:
        collection = db[device_id]
        print(collection)
        booleanhbase = False
        DeviceKwh_list = []
        for index in range(len(timerange) - 1):
            mongoTime = timerange[index]
            sum_kwh = 0
            rowkeyvalue1 = timerange[index].strftime("%Y%m%d%H%M%S")
            rowkeyvalue1+='000'
            rowkeyvalue2 = timerange[index+1].strftime("%Y%m%d%H%M%S")
            rowkeyvalue2 = rowkeyvalue2+'000'
            try:
                print('here')
                for post in collection.find({'Capaturetime':{'$gt':timerange[index],'$lte':timerange[index+1]}}):
                    sum_kwh += post['KWH']
                    mongoTime =  post['Capaturetime']   # Timelist.append(timerange[index])
                print(timerange[index],sum_kwh)
                DeviceKwh_list.append(sum_kwh)
                Devicedict[device_id] = DeviceKwh_list
                if int(mongoTime.strftime("%Y%m%d%H%M%S")) < int(timerange[index+1].strftime("%Y%m%d%H%M%S")):
                    booleanhbase = True
                    print('mongotime',int(mongoTime.strftime("%Y%m%d%H%M%S")))
                    print('ff',int(timerange[index+1].strftime("%Y%m%d%H%M%S")))
            except:
                DeviceKwh_list.append(0)
                Devicedict[device_id] = DeviceKwh_list

            if booleanhbase:
                try:
                    pool = happybase.ConnectionPool(size=3,host='localhost')
                    print("hbase in")
                    rowkeyvalue1 = mongoTime.strftime("%Y%m%d%H%M%S")
                    rowkeyvalue1+='000'
                    with pool.connection() as connection:
                        table = connection.table(device_id)
                        count = 0
                        for key, data in table.scan(row_start = rowkeyvalue1,columns = [b'KWH:KWH'], row_stop = rowkeyvalue2):
                            bytedara = data[b'KWH:KWH']
                            decodevute = float(bytedara.decode("ascii"))
                            count+=1
                            sum_kwh += decodevute
                        print(count,sum_kwh)

                        DeviceKwh_list.append(sum_kwh)
                        Devicedict[device_id] = DeviceKwh_list

                except:
                    print("hbase fail")
                    DeviceKwh_list.append(0)
                    Devicedict[device_id] = DeviceKwh_list
                booleanhbase = False
            else:
                pass
    client.close()
    x = dumptoJson(devices,x,timerange,Devicedict)
    return x
    # for r in devices

# x = my_time.mytime('2017-01-01 2:10:00','2017-01-01 3:10:00',1)
# y = Rangequeryv2(['kdd91201'],'2016-01-01 2:10:00','2016-01-01 4:10:00',1)
# print(y)
map = bson.Code("""
            function(){

                     emit(this.Capaturetime,parseFloat(this.KWH))
                   }

                """)
reduce = bson.Code("""
                    function(key, values)
                    {
                              var result = 0;
                              for (var i = 0; i < values.length; i++) {
                                  result += values[i];
                                  }
                              return result;
                    }
                    """)
#
# client = MongoClient('localhost')
# db = client.test_webbase
# sr = datetime.strptime("2016/1/1 0:0", "%Y/%m/%d %H:%M")
# lr = datetime.strptime("2016/4/1 0:15", "%Y/%m/%d %H:%M")
#
#
# """
# """
#
# group = {'_id': None,'count': {'$sum': '$KWH'},'lasttime':{'$last':'$Capaturetime'}}
# group1 = {'_id': None,'firsttime':{'$first':'$Capaturetime'},'firstkwh':{'$first':'$KWH'},'lastkwh':{'$last':'$KWH'},'lasttime':{'$last':'$Capaturetime'}}
# # group['_id'] = "$Capaturetime"
# # group['$all_kwh'] = {
# #    '$sum' : '$KWH',     #对view_pv字段求和
# # }
# # sort = {
# #    '_id' : 1,
# #    'all_kwh'  :1, #all_view_ip来自于上面group当中的key,-1和1分别表示倒序和升序
# # }
# # aggs = [
# #         {"$match": {"Capaturetime":{'$gt':sr,'$lte':lr}}},
# #         {"$project": SON{"Capaturetime":1, "KWH":1}},
# #
# #
# # ]
#
#
# print(db.kdd91201.find_one())
# print(sr,lr)
# import time
# # res = db.kdd91201.map_reduce(map, reduce,{out:"oresult", query:{Capaturetime:{'$gt':sr,'$lte':lr}}})
# # x = db.kdd91201.aggregate([{'$group':{'_id':'1','all_kwh':{'$sum':'$KWH'}}},{'$match':{'Capaturetime':{'$gt':sr,'$lte':lr}}}])
# tStart = time.time()#計時開始
# rr =  db.kdd91203.aggregate([{'$match': match},{'$group': group1}])
# # y = db.kdd91203.find_one({'Capaturetime':{'$gt':sr,'$lte':lr}})
# # print(y)
# # print(rr)
# print(list(rr))
# tend = time.time()#計時開始
# print(tend - tStart)
# m_Rangequery([1],'2017-05-09 2:10:00','2017-05-10 3:10:00',2)
