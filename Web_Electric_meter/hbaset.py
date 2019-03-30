# coding=UTF-8
import happybase
import meter
import datetime
import random
DeviceIdList = ['kdd91201','kdd91202','kdd91203','kdd91204','kdd91205','kdd91206','kdd91207','kdd91208','kdd91209','kdd91210']
DeviceId2List = ['kdd91201','kdd91202','kdd91203']
datadict = { 'Capaturetime':dict(),'VLN_A': dict(), 'VLN_B': dict(), 'VLN_C': dict(), 'I_A': dict(), 'I_B': dict(), 'I_C': dict(),'KW_A': dict(), 'KW_B': dict(),
            'KW_C': dict(), 'KVAR_A': dict(), 'KVAR_B': dict(), 'KVAR_C': dict(),'KWH': dict(), 'KVARH': dict(),}
print(datadict)
va = 110
vb = 110
vc = 110
ia = 1.05
ib = 1.05
ic = 1.05
ka = 115.5
kb = 115.5
kc = 115.5
kwh = 0.049
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
connection = happybase.Connection('localhost')
connection.open()
print(connection.tables())
x = connection.tables()
for r in x:
    connection.disable_table(r)
    connection.delete_table(r)
    # connection.create_table(r, datadict)
    print(r,'success')
for r in DeviceId2List:
    connection.create_table(r, datadict)
    print(r,'success')
print(connection.tables())
timelist = []
YearList = [2016,2017]

DateList = [31,28,31,30,31,30,31,31,30,31,30,31]
mms = ['000','500']
for mon in range(2, 3):
    for r in range(1, DateList[mon-1]+1):
        for hour in range(24):
            for mmin in range(60):
                for ms in range(60):
                    for mmms in mms:
                        stime = datetime.datetime(2016, mon, r, hour, mmin, ms).strftime("%Y%m%d%H%M%S")
                        stime = stime+mmms
                        timelist.append(stime)
DeviceIdrList = ['kdd91201','kdd91202','kdd91203']
# for tabs in DeviceIdrList:
#     connection.disable_table(tabs)
#     connection.delete_table(tabs)
#     connection.create_table(tabs, datadict)
def CreateTestData():
    # connection = happybase.Connection('localhost')
    # connection.open()
    print('go')
    print(connection.tables())
    for tabs in DeviceIdrList:
        table = connection.table(tabs)
        kwh = 33611.2416
        with table.batch(batch_size=2000) as b:

            for mtime in timelist:
                kwh+=0.0062745
                test = meter.Meter(mtime, va, vb, vc, ia, ib, ic, ka, kb, kc, 0, 0, 0, kwh, 0)
                b.put(row=mtime, data=test.Meterdict())

    #
    # for tab in DeviceIdList:
    #     table = connection.table(tab)
    #     timelist = []
    #     for mon in range(4, 5):
    #         for r in range(1, DateList[mon-1]+1):
    #             for hour in range(24):
    #                 print(tab,mon,r,hour)
    #                 for mmin in range(60):
    #                     for ms in range(60):
    #                         for mmms in mms:
    #                             stime = datetime.datetime(2016, mon, r, hour, mmin, ms, mmms).strftime("%Y%m%d%H%M%S")
    #                             stime = stime+str(mmms)
    #                             timelist.append(stime)
    #                             # sstime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #                                 # collection = db[DeviceIdList[i]]
    #                             va = 110
    #                             vb = 110
    #                             vc = 110
    #                             ia = 1.05
    #                             ib = 1.05
    #                             ic = 1.05
    #                             ka = 115.5
    #                             kb = 115.5
    #                             kc = 115.5
    #                             kwh = 0.049
    #                             test = meter.Meter( stime, va, vb, vc, ia, ib, ic, ka, kb, kc, 0, 0, 0, kwh, 0)
    #                             table.put(row=stime, data=test.Meterdict(), timestamp = int(stime))
    #                                 # row = table.row(stime)
    #                                 # print(row)
    #                                 # print(test.Meterdict())
    # #                            print(stime)
CreateTestData()
connection.close()
# CreateTestData()
# # connection.close()
# row = table.row(b'row-key')
