from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
from urllib.parse import urlencode
import csv


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):

    bus_stations_list = []

    with open(settings.BUS_STATION_CSV, newline='', encoding='cp1251') as file:
        reader = csv.DictReader(file)
        for row in reader:
            bus_stations_list.append({'Name': row['Name'], 'Street': row['Street'], 'District': row['District']})

    current_page = int(request.GET.get('page', 1))
    paginator = Paginator(bus_stations_list, 10)
    page = paginator.get_page(current_page)
    new_data = page.object_list

    if page.has_next() == True:
        next_page_url = '?'.join((reverse('bus_stations'), urlencode({'page': page.next_page_number()})))
    else:
        next_page_url = None
    if page.has_previous():
        prev_page_url = '?'.join((reverse('bus_stations'), urlencode({'page': page.previous_page_number()})))
    else:
        prev_page_url = None
    return render(request, 'index.html', context={
        'bus_stations': new_data,
        'current_page': page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url
    })

