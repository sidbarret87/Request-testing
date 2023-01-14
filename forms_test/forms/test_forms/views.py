from django.shortcuts import render
from django.http import HttpResponse
from tinydb import TinyDB, Query, where
import requests
import json
import re
results_search_fromDb=[]
test_requests = [{'request':'email_field=gvidoVanRossum@mail.ru&date_field=10.01.1987'},
                 {'request':'email_field=gravedigger@mail.com&phone_field=+7 123 456 78 90'},
                 {'request':'email=gravedigger@mail.com&phone_field=+7 123 456 78 90'},
                 {'request':'date=10.12.2022&my_email=slayer@mail.ru'},
                 {'request':'date_field=10.12.2022&my_email=slayer@mail.ru'}
                 ]
val = None


def test(request):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    for req in test_requests:
        r = requests.post('http://127.0.0.1:8000/get_form/', data=req['request'], headers=headers)
    return HttpResponse(r)

def form(request):
    elements_in_list = (len(test_requests)) # сколько словарей в списке
    db = TinyDB('db.json')
    values=None
    def search_in_db():
        result=None
        keys=list()
        values=list()
        req={}
        for key, value in request.POST.items():

            keys.append(key)
            values.append(validation(value))

            req[key]=validation(value)
            # сформирован словарь вида {'email_field': 'email', 'date_field': 'date'}
        match len(keys):
            case 2:
                result=db.search( (where(keys[0]) == f'{(values[0])}') & (where(keys[1]) == f'{(values[1])}'))
                print(f"Результат поиска из базы данных {result}")
                if (result!=[]):
                    return result[0]['name']
                else:
                    return json.dumps(req)


    def validation(value_):
        if re.search(r"^(3[01]|[12][0-9]|0[1-9]).(1[0-2]|0[1-9]).[0-9]{4}$",value_):
            return 'date'
        elif re.search(r'^\d{4}-\d{2}-$\d{2}',value_):
            return 'date'
        elif re.search(r'7 \d\d\d\ \d\d\d \d\d \d\d',value_):
            return 'phone'
        elif re.search(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+',value_):
            return 'email'
        else:
            return 'text'


    val=search_in_db()
    results_search_fromDb.append(val)
    for i in range(elements_in_list):
        # добавляем в основной словарь результат по запросу
        test_requests[i]['value']=results_search_fromDb[i]


    #db.insert({'name': 'date, text', 'date_field':'date', 'text_field':'text'})

    print(results_search_fromDb)
    return render(request, 'test_forms/index.html',{
        'test_requests':test_requests,
        })

# Create your views here.
