from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from .models import Newsletter, Message, Client, StatisticsNewletter


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'


class StatisticsNewletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticsNewletter
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


# class ClientModel:
#     def __init__(self, phone_number, client_operator_code, client_tag, timezone):
#         self.phone_number = phone_number
#         self.client_operator_code = client_operator_code
#         self.client_tag = client_tag
#         self.timezone = timezone


# class ClientSerializer(serializers.ModelSerializer):
#     phone_number = serializers.CharField(max_length=11)
#     client_operator_code = serializers.CharField(max_length=10)
#     client_tag = serializers.CharField(max_length=255)
#     timezone = serializers.CharField(max_length=50)
#
#     def create(self, validated_data):
#         return Client.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.phone_number = validated_data.get('phone_number', instance.phone_number)
#         instance.client_operator_code= validated_data.get('client_operator_code', instance.client_operator_code)
#         instance.client_tag = validated_data.get('client_tag', instance.client_tag)
#         instance.timezone = validated_data.get('timezone', instance.timezone)
#         instance.save()
#         return instance
#




# def encode():
#     model = ClientModel(1234, 123, 'fff', 'Russia')
#     model_sr = ClientSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
