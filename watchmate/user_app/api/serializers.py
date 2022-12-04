from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={'input_style': 'password'})
    class Meta:
        model = User
        fields= ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only' : True},
        }
        
    def save(self, *args, **kwargs):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise ValidationError("Password and password2 do not match")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        
        account = User(username=username, email=email)
        account.set_password(password)
        account.save()
        
        return account
        
        