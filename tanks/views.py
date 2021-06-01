from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from django.template import loader
from django.http import HttpResponse
from django import template
from django.shortcuts import render
from django.db.models import Max
from django_xhtml2pdf.utils import generate_pdf
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
import datetime
from collections import defaultdict
from rest_framework.serializers import Serializer
from django.forms.models import model_to_dict
from .models import Zbiornik, Badanie
from homolog.models import Rodzaj
from .serializers import ZbiornikSerializer, BadanieSerializer
import json
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

@login_required(login_url="/login/")
def index(request):
    context = {
        "badania" : "active", 
        "count" : Zbiornik.objects.all().count(),
        "zbiorniki":Zbiornik.objects.all()
        }
    return render(request, "badania.html",context)

@login_required(login_url="/login/")
def view(request, id):
    context = {
        "zbiornik" : Zbiornik.objects.get(id=id), 
        "badania" : Badanie.objects.filter(zbiornik_id=id).order_by('cisnienie'),
        }
    return render(request, "badania_view.html",context)

@login_required(login_url="/login/")
def tank_edit(request):
    if request.method == 'POST':
        index = request.POST['id']
        numer = request.POST['numer']
        nr_odbioru = request.POST['nr_odbioru']
        nr_rozrywania = request.POST['nr_rozrywania']
        pekniecie = request.POST['pekniecie']
        Zbiornik.objects.filter(pk=index).update(numer=numer,nr_odbioru=nr_odbioru,nr_rozrywania=nr_rozrywania,pekniecie=pekniecie)
        response_data = {}
        response_data['result'] = 'Sussces'
        response_data['message'] = 'wow wsio oki'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return redirect("/badania/")


@login_required(login_url="/login/")   
def delete(request, id):  
    rodzaj = Zbiornik.objects.get(id=id)  
    rodzaj.delete()
    return redirect("/badania/")
 
def myview(response, id):
    pres = {'t': Badanie.objects.filter(zbiornik_id=id).aggregate(Max('cisnienie')),}
    pres = pres['t']['cisnienie__max']
    pres = float(pres / 10)
    poj = Zbiornik.objects.get(id=id)
    print(poj.rodzaj.capacity)
    woda = {'w':Badanie.objects.filter(zbiornik_id=id).aggregate(Max('woda'))}
    woda = woda['w']['woda__max']
    procent= woda / poj.rodzaj.capacity * 100
    print(procent)
    data = {
        'today': datetime.date.today(), 
        'tank':  Zbiornik.objects.get(id=id),
        'badania': Badanie.objects.filter(zbiornik_id=id).order_by('cisnienie'),
        'pres': pres,
        'woda' : woda,
        'procent' : procent,
        'typ' : poj.rodzaj.tank
        }

    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('print.html', context=data, file_object=resp)
    return result

@api_view(['GET'])
def ZbiornikAll(request):
    queryset = Zbiornik.objects.all()
    serializer = ZbiornikSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ZbiornikId(request, id):
    queryset = Zbiornik.objects.get(id=id)
    serializer = ZbiornikSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def BadanieTank(request):
    queryset = Badanie.objects.all()
    serializer = BadanieSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def BadanieTankId(request, id):
    queryset = Badanie.objects.filter(zbiornik=id)
    serializer = BadanieSerializer(queryset, many=True)
    newDict= {'data': {}, 'zbiornik':{ }}
    newDict['data'] = serializer.data
   
    zbiornik = Zbiornik.objects.get(id=id)
    obj = model_to_dict(zbiornik)
    newDict['zbiornik']['zbiornik']= obj
    pk= (newDict['zbiornik']['zbiornik']['rodzaj'])
    rodzaj = Rodzaj.objects.get(id=pk)
    obj = model_to_dict(rodzaj)
    newDict['zbiornik']['homolog'] = obj
    woda = Badanie.objects.filter(zbiornik=id).values_list('woda',flat=True)
    cisnienie = Badanie.objects.filter(zbiornik=id).values_list('cisnienie',flat=True)
    newDict['zbiornik']['maxWoda']= max(woda)
    newDict['zbiornik']['woda']= woda
    newDict['zbiornik']['maxCisnienie']= max(cisnienie)
    newDict['zbiornik']['cisnienie']= cisnienie
    return Response(newDict)

@api_view(['GET'])
def BadanieTankListId(request, id):
    queryset = Badanie.objects.filter(zbiornik=id).values_list('woda',flat=True)
    woda = list(queryset)
    newDict = {'woda': [], 'czas':[],'cisnienie':[]}
    newDict['woda'].extend(woda)
    queryset = Badanie.objects.filter(zbiornik=id).values_list('czas',flat=True)
    czas = list(queryset)
    newDict['czas'].extend(czas)
    queryset = Badanie.objects.filter(zbiornik=id).values_list('cisnienie',flat=True)
    cisnienie = list(queryset)
    newDict['cisnienie'].extend(cisnienie)

    return Response(newDict)

@api_view(['DELETE'])   
def BadanieDelete(request, id):  
    rodzaj = Zbiornik.objects.get(id=id)  
    rodzaj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
 
# szukanie zbiornika mqtt
@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'body': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
        }))
@api_view(['POST'])
def TankSearch(request):
    symbol = request.data["id"]
    numer = request.data["numer"]
    odpowiedz = {
        'jest_zbiornik' : False,
        'msg': False,
        'msg_bad' : False,
        'nr_odbioru':0,
        'nr_rozrywania':0,
        'btn_save_next': False,
        'btn_save': False
    }
    if (len(numer) == 4):
        try:
            queryset = Zbiornik.objects.get(rodzaj=symbol, numer=numer)
            odpowiedz['msg'] = True
            return Response(odpowiedz)
        except ObjectDoesNotExist :
            q_odbioru = Zbiornik.objects.all().order_by('nr_odbioru').last()
            datanow = datetime.date.today().strftime("%Y-%m-%d")
            data_zb = datetime.datetime.strftime(q_odbioru.dataBadania, "%Y-%m-%d" )
            print(q_odbioru.dataBadania, datanow )
            if (data_zb == datanow):
                nr_rozrywania = Zbiornik.objects.filter(dataBadania =datanow).order_by('nr_rozrywania').last()
                nr_rozrywania = nr_rozrywania.nr_rozrywania + 1
                nr_odbioru = q_odbioru.nr_odbioru
                print("numer rozrywania", nr_rozrywania)
            else :
                nr_odbioru = q_odbioru.nr_odbioru + 1
                nr_rozrywania = 1
                
            print(nr_odbioru , nr_rozrywania)
            odpowiedz['jest_zbiornik'] = True
            odpowiedz['nr_odbioru'] = nr_odbioru
            odpowiedz['nr_rozrywania'] = nr_rozrywania

            return Response(odpowiedz)
    else:
        print('numer nie ma 4 cyfr')
        odpowiedz['msg_bad'] = True
        return  Response(odpowiedz)
# zapisanie zbiornika mqtt
@api_view(['POST'])
def TankAdd(request):
    id_homolog = request.data["rodzaj"]
    rodzaj = Rodzaj.objects.get(id=id_homolog)
    numer = request.data["numer"]
    data = datetime.date.today().strftime("%Y-%m-%d")
    nr_odbioru = request.data['nr_odbioru']
    nr_rozrywania = request.data['nr_rozrywania']
    tank = Zbiornik(numer=numer,rodzaj=rodzaj,dataBadania=data,nr_odbioru=nr_odbioru,nr_rozrywania=nr_rozrywania)
    tank.save()
    return Response({'btn_save_next': True,'tank_id': tank.id, 'btn_save': True})

@api_view(['POST'])
def SaveBadanie(request):
    id_zbiornik= request.data["zbiornik"]
    zbiornik = Zbiornik.objects.get(id=id_zbiornik)
    woda = request.data["woda"]
    cisnienie = request.data['cisnienie']
    czas = datetime.datetime.now().strftime("%H:%M:%S")
    badanie = Badanie(zbiornik=zbiornik, woda=woda,cisnienie=cisnienie,czas=czas)
    badanie.save()
    return Response({"save":True})