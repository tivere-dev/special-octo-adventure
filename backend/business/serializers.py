from rest_framework import serializers
from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'business_name', 'currency', 'business_logo', 'business_type', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_business_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Business name must be at least 2 characters long.')
        return value

    def validate_business_logo(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError('Logo file size must not exceed 5MB.')
            
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError('Only JPEG and PNG images are allowed.')
        
        return value


class BusinessSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['business_name', 'currency', 'business_logo']

    def validate_business_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Business name must be at least 2 characters long.')
        return value

    def validate_business_logo(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError('Logo file size must not exceed 5MB.')
            
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError('Only JPEG and PNG images are allowed.')
        
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        
        if hasattr(user, 'business'):
            raise serializers.ValidationError('User already has a business setup.')
        
        business = Business.objects.create(user=user, **validated_data)
        return business


class BusinessUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['business_name', 'currency', 'business_logo']

    def validate_business_name(self, value):
        if value and len(value) < 2:
            raise serializers.ValidationError('Business name must be at least 2 characters long.')
        return value

    def validate_business_logo(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError('Logo file size must not exceed 5MB.')
            
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError('Only JPEG and PNG images are allowed.')
        
        return value
