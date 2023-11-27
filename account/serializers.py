from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(
        min_length=8, write_only=True, required=True
    )
    password2 = serializers.CharField(
        min_length=8, write_only=True, required=True
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = '__all__'


    def validate(self, attrs):
        # print(attrs, '!!!!!')
        password2 = attrs.pop('password2')
        if password2 != attrs['password']:
            raise serializers.ValidationError('Passwords didn\'t matsh!')
        validate_password(attrs['password'])
        return attrs
    def validate_first_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError(
                'Name must start with uppercase letter!')
        return value








