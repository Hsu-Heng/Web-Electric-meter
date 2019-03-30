# coding=UTF-8
"""
Version: 1
Creater: Hsu
Detail: No ood
"""
from datetime import datetime, date, time, timedelta
class mytime():
    def __init__(self,time1,time2,searchtype):
        self.time1 = time1
        self.time2 = time2
        self.searchtype = searchtype


    def calculatetime(self):
        try:
            d_time1 = datetime.strptime(self.time1, "%Y-%m-%d %H:%M:%S:%f")
            d_time2 = datetime.strptime(self.time2, "%Y-%m-%d %H:%M:%S:%f")
        except:
            d_time1 = datetime.strptime(self.time1, "%Y-%m-%d %H:%M:%S")
            d_time2 = datetime.strptime(self.time2, "%Y-%m-%d %H:%M:%S")
        if d_time2 > d_time1:

            dif = d_time2 - d_time1
            # print(dif)
            allseconds = int(dif.total_seconds())
            min_secounds = 60
            hour_secounds = min_secounds * 60
            day_secounds = hour_secounds * 24
            day_secounds = hour_secounds * 24
            if self.searchtype == 1:
                # addtime = timedelta(minutes = 15)
                tilelist = []
                Divisible15mim = (allseconds // ( min_secounds * 15))+1
                for i in range(0, Divisible15mim):
                    tilelist.append(d_time1 + timedelta(minutes = 15 * i))
                if allseconds % ( min_secounds * 15) > 0:
                    tilelist.append(d_time2)
                # tilelist.append(d_time2)
                return tilelist
            elif self.searchtype == 2:
                tuple_time1 = d_time1.timetuple()
                tuple_time2 = d_time2.timetuple()
                dd_time1 = datetime(tuple_time1[0], tuple_time1[1],tuple_time1[2],0,0,0)
                tilelist = []
                Divisibleday = (allseconds // day_secounds)+1
                tilelist.append(d_time1)
                for i in range(1, Divisibleday):
                    tilelist.append(dd_time1 + timedelta(days = i))
                if allseconds % ( day_secounds) > 0:
                    tilelist.append(d_time2)
                return tilelist
            elif self.searchtype == 3:
                tuple_time1 = d_time1.timetuple()
                tuple_time2 = d_time2.timetuple()
                year = tuple_time2[0] - tuple_time1[0]
                month = tuple_time2[1] - tuple_time1[1]
                difmonth = (12 * year) + month

                timelist = []
                timelist.append(d_time1)
                for i in range(1,difmonth+1):

                    try:
                        timelist.append(datetime(tuple_time1[0], tuple_time1[1] + i,1,0,0,0))
                    except:
                        timelist.append(datetime(tuple_time1[0] + ((tuple_time1[1] + i)//12), (tuple_time1[1] + i)%12,1,0,0,0))
                if(timelist[-1]!=d_time2):
                    timelist.append(d_time2)
                return timelist
            elif self.searchtype == 4:
                tuple_time1 = d_time1.timetuple()
                tuple_time2 = d_time2.timetuple()
                year = tuple_time2[0] - tuple_time1[0]
                timelist = []
                if year == 0:
                    timelist.append(d_time1)
                    if(timelist[-1]!=d_time2):
                        timelist.append(d_time2)
                    return timelist
                else:
                    timelist.append(d_time1)
                    for i in range (0 , year+1):
                        if datetime(tuple_time1[0] + i, 1,1,0,0,0)!= d_time1:
                            timelist.append(datetime(tuple_time1[0] + i, 1,1,0,0,0))

                    timelist.append(d_time2)
                    # list2 = []
                    # for r in timelist:
                    #     if not r in list2:
                    #         list2.append(r)
                    return timelist
