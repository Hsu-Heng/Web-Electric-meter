from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

from pymongo import MongoClient
from datetime import datetime, date, time, timedelta
from metertest import my_time
import happybase
import json
from metertest import mongoconnection
def helloParams(request,param1,param2):
    return HttpResponse("p1 = " + param1 + "; p2 = " + param2+ "; p3 = " + param3)
def apiall(request,param1,param2,param3):
    t1 = param1
    t2 = param2
    drange = int(param3)
    timerange = my_time.mytime(t1, t2, drange).calculatetime()
    print(timerange)
    return HttpResponse(str(timerange))
def api(request,param1,param2,param3,param4):
    return HttpResponse("p1 = " + param1 + "; p2 = " + param2+ "; p3 = " + param3+ "; p3 = " + param4)
def home(request):
    return render(request, 'test.html')
def my_post(request):
    if 'ok' in request.POST:

        time1 = request.POST['begin_time']
        time2 = request.POST['end_time']
        try:
            searchtype = request.POST['queryrange']
        except:
            searchtype = 1
        devicedlist = []
        try:
            device_id = request.POST['device_id']
            if device_id == "":
                devicedlist = []
            else:
                devicedlist = device_id.split('-')
        except:
            devicedlist = []
        print(time1,time2,searchtype,device_id)
        return HttpResponse(json.dumps(mongoconnection.Rangequeryv2(devicedlist, time1, time2, int(searchtype))),content_type="application/json")
    return render(request, 'test.html')

def test(request):
    # y = Rangequeryv2([],'2016-01-01 0:00:00','2016-1-1 1:00:00',1)
    return render(request, 'test.html')
    # print(y)
    # return HttpResponse(json.dumps(y),content_type="application/json")
