from rest_framework import serializers
from .models import PowerSupply, SerialCollector, FPGA

class PowerSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerSupply
        fields = '__all__'

class SerialCollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerialCollector
        fields = '__all__'

class FPGASerializer(serializers.ModelSerializer):
    connected_power_supply = PowerSupplySerializer()
    connected_serial_collector = SerialCollectorSerializer()

    class Meta:
        model = FPGA
        fields = '__all__'