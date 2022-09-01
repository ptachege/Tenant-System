from rest_framework import serializers
from .models import *


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = '__all__'


class CaretakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caretaker
        fields = '__all__'


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'
