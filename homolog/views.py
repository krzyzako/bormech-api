from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from .serializers import HomologSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django import template
from .models import Rodzaj
from .forms import RodzajForm
from rest_framework.schemas import AutoSchema
from rest_framework.compat import coreapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from drf_yasg import openapi

class CustomSampleSchema(AutoSchema):
    def __init__(self):
        super(CustomSampleSchema, self).__init__()

    def get_manual_fields(self, path, method):
        extra_fields = [
            coreapi.Field('field1', required=True, location='form', description='', type='', example=''),
            coreapi.Field('field2', required=False, location='form', description='', type='', example=''),
            coreapi.Field('field3', required=False, location='form', description='', type='', example='')

        ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

class OtherStuffSerializer(serializers.Serializer):
    foo = serializers.CharField()



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def HomologAll(request):
    queryset = Rodzaj.objects.all()
    serializer = HomologSerializer(queryset, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def ViewId(request, id):
    queryset = Rodzaj.objects.get(id=id)
    serializer = HomologSerializer(queryset, many=False)
    
    return Response(serializer.data)

test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
user_response = openapi.Response('response description', HomologSerializer)

# @swagger_auto_schema(method='post', responses={200: user_response})
@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'body': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
        }))
@permission_classes((IsAuthenticated, ))
@api_view(['POST'])
def HomologAdd(request):
    serializer = HomologSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        print('ok')
        serializer.save()
    else :
        print('no')
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def HomologUpdate(request, pk):
    queryset = Rodzaj.objects.get(id=pk)
    serializer = HomologSerializer(queryset, data=request.data)
    if serializer.is_valid():
        serializer.save()
       
    return Response(serializer.data)
 
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def HomologDetail(request, pk):
    try:
        queryset = Rodzaj.objects.get(id=pk)
        serializer = HomologSerializer(queryset, many=False)
        return Response(serializer.data)
    except ObjectDoesNotExist :
        return Response({'msg':"error"})

@api_view(['DELETE'])
@permission_classes((IsAuthenticated, ))
def HomologDelete(request, pk):
    try:
        queryset = Rodzaj.objects.get(id=pk)
        queryset.delete()
        return Response({'msg':'success'})
    except ObjectDoesNotExist :
        return Response({'msg':"error"})

@api_view(['GET'])
def HomologChoise(request):
    return Response(Rodzaj.typ)

@api_view(['GET'])
def UserGet(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def HomologBySymbol(request, symbol):
    try:
        queryset = Rodzaj.objects.get(symbol=symbol.upper())
        serializer = HomologSerializer(queryset, many=False)
        newdict={'bit': True,'reset' : False,'error': False}
        newdict.update(serializer.data)
        newdict["poj"] = newdict.pop("capacity")
        newdict["homologacja"] = newdict.pop("approval")
        newdict["waga"] = newdict.pop("weight")
        newdict["srednica"] = newdict.pop("dimeter")
        newdict["typ"] = newdict.pop("tank")
        del newdict['tank_display']
        return Response(newdict)
    except ObjectDoesNotExist :
        odpo = {'bit': False,'reset' : True,'error': True,'poj': 0,'homologacja': '','waga': 0,'srednica': 0,'id':0,'typ':0}
        return Response(odpo)