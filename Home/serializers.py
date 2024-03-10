from rest_framework import serializers
from .models import ThongTinBenhNhan, Queue, Service, Doctor
from rest_framework import serializers
from django.contrib.auth.models import User

class ThongTinBenhNhanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThongTinBenhNhan
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'        

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password1','email', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError({'password1': 'Mat khau khong trung khop'})
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password1', None)
        validated_data.pop('password2', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
