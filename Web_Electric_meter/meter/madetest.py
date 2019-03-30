# coding=UTF-8
#!/home/hsu/anaconda3/bin python
"""It's a test."""
import sys
print(sys.version)
import metercalss
import pymongo
import json
import datetime
import time
import random
client = pymongo.MongoClient('localhost', 27017)
client.drop_database('test_webbase')
print('delete')
db = client.test_webbase

def GenerateVoltiage():
    t_interger = 108
    t_offset = random.uniform(1.5, 3.2)
    return t_interger+t_offset
def GenerateCurrent():
    t_offset = random.uniform(0, 10)
    return t_offset
def CaculatePower(Voltiage, Current):
    return Voltiage * Current
def CalculateKwh(power1, power2, power3):
    return (power1+ power2+ power3) / 72000
def CreateTestData():

    DeviceIdList = ['kdd91201','kdd91202','kdd91203']
    YearList = [2016]
    DateList = [31,28,31,30,31,30,31,31,30,31,30,31]
    mms = [0,500000]
    for row in DeviceIdList:
        collection = db[row]
        kwhlist = 0
        print(row)
        for mon in range(1, 2):
            for day in range(1, DateList[mon-1]+1):
                for hour in range(24):
                    for mmin in range(60):
                        for ms in range(60):
                            for mmms in mms:
                                stime = datetime.datetime(2016, mon, day, hour, mmin, ms, mmms)
                                va = 110.0
                                vb = 110.0
                                vc = 110.0
                                ia = 1.0
                                ib = 1.5
                                ic = 1.6
                                ka = 110.0
                                kb = 165.2
                                kc = 176.2
                                kwhlist += 0.0062745
                                test = metercalss.Meter( stime, va, vb, vc, ia, ib, ic, ka, kb, kc, 0, 0, 0, kwhlist, 0)
                                collection.insert(test.Meterdict())
                    print(2016, mon, day, hour, mmin)
CreateTestData()
