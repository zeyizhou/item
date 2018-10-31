import json
import random
import time
import datetime
import requests
from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic
from django.urls import reverse_lazy

from .models import Item
from .forms import SNCF, UploadFileForm


def index(request):
    all_item_list = Item.objects.order_by ('-price')
    context = {
        'all_item_list': all_item_list,
    }
    return render (request, 'price/index.html', context)


class DetailView (generic.DetailView):
    model = Item
    template_name = 'price/detail.html'


class PersonCreateView (generic.CreateView):
    model = Item
    template_name = 'price/add.html'
    fields = '__all__'


    success_url = reverse_lazy ('price:index')


class ItemUpdate (generic.UpdateView):
    model = Item
    fields = '__all__'
    template_name = 'price/update.html'
    success_url = reverse_lazy ('price:index')


class ItemDelete (generic.DeleteView):
    model = Item
    success_url = reverse_lazy ('price:index')


def search_item(request):
    ''' This could be your actual view or a new one '''
    # Your code
    if request.method == 'GET':
        # If the form is submitted
        search_query = request.GET.get ('search_box', None)
        all_item_list = Item.objects.filter (name__contains=search_query)
        context = {
            'all_item_list': all_item_list,
        }
        return render (request, 'price/index.html', context)


def import_data(request):
    if request.method == "POST":
        form = UploadFileForm (request.POST,
                               request.FILES)

        if form.is_valid ():
            request.FILES['file'].save_to_database (
                model=Item,
                mapdicts=[
                    ['name', 'price', 'quantity', 'sold_quantity', 'pub_date']]
            )
            return redirect ('price/index')
        else:
            return HttpResponseBadRequest ()
    else:
        form = UploadFileForm ()
        return render (
            request,
            'upload_form.html',
            {
                'form': form,
                'title': 'Import excel data into database example',
                'header': 'Please upload sample-data.xls:'
            })


# TGV
def get_ticket(request):
    if request.method == 'POST':
        form = SNCF (request.POST)
        if form.is_valid ():
            postUrl = 'https://www.oui.sncf/proposition/rest/best-prices/in-range'
            # payloadData数据
            index = 3
            HCode = "HC200211251"
            departureDate = request.POST.get ("departureDate") + "T06:00:00"
            date = datetime.datetime.strptime (departureDate, '%Y-%m-%dT%H:%M:%S')
            today = datetime.datetime.now ()
            date1 = datetime.datetime.strptime (request.POST.get ("departureDate"), '%Y-%m-%d')

            birthDate = "1995-03-15T00:00:00"
            if (date + datetime.timedelta (days=-3)).strftime ('%Y-%m-%d') > time.strftime ('%Y-%m-%d',
                                                                                            time.localtime (
                                                                                                time.time ())):
                rangeStart = (date + datetime.timedelta (days=-3)).strftime ('%Y-%m-%dT%H:%M:%S')
            else:
                rangeStart = time.strftime ('%Y-%m-%dT%H:%M:%S', time.localtime (time.time ()))

                index = (date1 - today).days + 1
            rangeEnd = (date + datetime.timedelta (days=+3)).strftime ('%Y-%m-%dT%H:%M:%S')

            origin = request.POST.get("origin")

            destination = request.POST.get("destination")

            user_agents = [
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
                "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
                "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
                "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
                "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            ]

            print (date)
            payloadData = {"query":
                               {"origin": origin,
                                "originCode": "",
                                "originLocation":
                                    {"id": None,
                                     "label": None,
                                     "longitude": None,
                                     "latitude": None,
                                     "type": None,
                                     "country": None,
                                     "stationCode": "",
                                     "stationLabel": None},
                                "destination": destination,
                                "destinationCode": "", "destinationLocation":
                                    {"id": None,
                                     "label": None,
                                     "longitude": None,
                                     "latitude": None,
                                     "type": None,
                                     "country": None,
                                     "stationCode": "",
                                     "stationLabel": None},
                                "via": None,
                                "viaCode": None,
                                "viaLocation": None,
                                "directTravel": True,
                                "asymmetrical": False,
                                "professional": False,
                                "customerAccount": False,
                                "oneWayTravel": True,
                                "departureDate": departureDate,
                                "returnDate": None,
                                "travelClass": "SECOND",
                                "country": "FR",
                                "language": "fr",
                                "busBestPriceOperator": None,
                                "passengers": [
                                    {"travelerId": None,
                                     "profile": "YOUNG",
                                     "age": 12,
                                     "birthDate": birthDate,
                                     "fidelityCardType": "NONE",
                                     "fidelityCardNumber": "",
                                     "commercialCardNumber": HCode,
                                     "commercialCardType": "HAPPY_CARD",
                                     "promoCode": None,
                                     "lastName": None,
                                     "firstName": None,
                                     "phoneNumer": None,
                                     "hanInformation": None}],
                                "animals": [],
                                "bike": "NONE",
                                "withRecliningSeat": False,
                                "physicalSpace": None,
                                "fares": [],
                                "withBestPrices": False,
                                "highlightedTravel": None,
                                "nextOrPrevious": False,
                                "source": "FORM_SUBMIT",
                                "targetPrice": None,
                                "han": False,
                                "outwardScheduleType": "BY_DEPARTURE_DATE",
                                "inwardScheduleType": "BY_DEPARTURE_DATE",
                                "currency": None,
                                "codeFce": None,
                                "companions": [],
                                "asymetricalItinerary": {}},
                           "rangeEnd": rangeEnd,
                           "rangeStart": rangeStart}
            user_agent = random.choice(user_agents)
            payloadHeader = {
                'Host': 'www.oui.sncf',
                'Accept': '*/*',
                'Accept-Language': 'zh,de;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6,zh-CN;q=0.5',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json;charset=UTF-8',
                "User-Agent": user_agent
            }
            # 下载超时
            timeOut = 25

            r = requests.post(postUrl, data=json.dumps (payloadData), headers=payloadHeader)
            dumpJsonData = json.dumps (payloadData)
            # print(f"dumpJsonData = {dumpJsonData}")
            res = requests.post (postUrl, data=dumpJsonData, headers=payloadHeader, timeout=timeOut,
                                 allow_redirects=True)
            new_dict = json.loads (res.text)
            result = ""
            print ("################################")
            if new_dict["dailyPrices"][index]["bestPrice"] == 0.0:
                for hour in new_dict["dailyPrices"][index]["hours"]:
                    result += str (hour['hour'])
                    result += "h \n"
            else:
                result = "No ticket this day"
            messages.info(request, result)
            return render (request, 'ticket.html',{'form': form})
    else:
        form = SNCF ()
    return render (request, 'ticket.html', {'form': form})
