from rest_framework import serializers
from .models import Products, Orders, Cart
from django.contrib.auth.models import User 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

class PizzaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class OrderSerializers(serializers.ModelSerializer):
    product = PizzaSerializers(read_only=True)
    customer = serializers.StringRelatedField(read_only=True)  

    class Meta:
        model = Orders
        fields = ['id', 'product', 'customer', 'quantity', 'order_time']

class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity']

class CartDetailSerializers(serializers.ModelSerializer):
    product = PizzaSerializers(read_only=True)  

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity']

class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    firstname = serializers.CharField(source='first_name')  
    lastname = serializers.CharField(source='last_name')
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all(), message="Tên đăng nhập đã tồn tại.")])
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'firstname', 'lastname']
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"error": "Hai mật khẩu không khớp."})
        return data
    def create(self, validated_data):
        validated_data.pop('password2')  
        user = User.objects.create_user(**validated_data)
        return user

class CustomLoginSerializers(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data.update({
            "status": "success",
            "message": f"Xin chào {self.user.first_name or 'Người dùng'}!"
        })
        return data