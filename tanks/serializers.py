from rest_framework import serializers
from .models import Zbiornik,Badanie
from homolog.models import Rodzaj
from django.contrib.auth.models import User

class HomologSerializer(serializers.ModelSerializer):
        model = Rodzaj
        fields = '__all__'

class ZbiornikSerializer(serializers.ModelSerializer):
    # tank_display = serializers.CharField(source='get_tank_display')
    typ = serializers.CharField(source='rodzaj.id')
    class Meta:
        model = Zbiornik
        fields = '__all__'

    # def create(self, validated_data):
    #     del validated_data['get_tank_display']
    #     return super(HomologSerializer, self).create(validated_data)


class BadanieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badanie
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']