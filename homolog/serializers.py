from rest_framework import serializers
from .models import Rodzaj
from django.contrib.auth.models import User

class HomologSerializer(serializers.ModelSerializer):
    tank_display = serializers.CharField(source='get_tank_display')
    class Meta:
        model = Rodzaj
        fields = '__all__'

    def create(self, validated_data):
        del validated_data['get_tank_display']
        return super(HomologSerializer, self).create(validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']