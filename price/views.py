import json

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
    all_item_list = Item.objects.order_by ('name')
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

    initial = {'pub_date': timezone.now ()}
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

            payloadHeader = {
                'Host': 'www.oui.sncf',
                'Content-Type': 'application/json;charset=UTF-8',
            }
            # 下载超时
            timeOut = 25

            r = requests.post (postUrl, data=json.dumps (payloadData), headers=payloadHeader)
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
