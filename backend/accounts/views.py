from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken as JWTRefreshToken
from django.conf import settings
from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from datetime import timedelta

from .models import User, EmailVerificationToken, PasswordResetToken, RefreshToken
from .serializers import (
    UserSerializer, SignupSerializer, LoginSerializer,
    ChangePasswordSerializer, PasswordResetRequestSerializer,
    PasswordResetSerializer, ProfileUpdateSerializer
)
from .utils import (
    create_email_verification_token, create_password_reset_token,
    send_verification_email, send_password_reset_email
)
from business.serializers import BusinessSerializer


def set_refresh_token_cookie(response, refresh_token, remember_me=False):
    max_age = 60 * 60 * 24 * (
        settings.JWT_REFRESH_TOKEN_LIFETIME_REMEMBER if remember_me
        else settings.JWT_REFRESH_TOKEN_LIFETIME_DEFAULT
    )
    
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        max_age=max_age,
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax'
    )


def clear_refresh_token_cookie(response):
    response.delete_cookie('refresh_token')


def create_tokens_for_user(user, remember_me=False):
    jwt_refresh = JWTRefreshToken.for_user(user)
    access_token = str(jwt_refresh.access_token)
    refresh_token_str = str(jwt_refresh)
    
    expires_at = timezone.now() + timedelta(days=(
        settings.JWT_REFRESH_TOKEN_LIFETIME_REMEMBER if remember_me
        else settings.JWT_REFRESH_TOKEN_LIFETIME_DEFAULT
    ))
    
    RefreshToken.objects.create(
        user=user,
        token=refresh_token_str,
        expires_at=expires_at
    )
    
    return access_token, refresh_token_str


@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='5/15m', method='POST')
def signup(request):
    serializer = SignupSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        verification_token = create_email_verification_token(user)
        send_verification_email(user, verification_token)
        
        user_serializer = UserSerializer(user)
        
        return Response({
            'user': user_serializer.data,
            'message': 'Account created successfully. Please check your email to verify your account.'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='5/15m', method='POST')
def login(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        remember_me = serializer.validated_data.get('remember_me', False)
        
        user.remember_me = remember_me
        user.update_activity()
        
        access_token, refresh_token = create_tokens_for_user(user, remember_me)
        
        user_serializer = UserSerializer(user)
        
        response_data = {
            'access_token': access_token,
            'user': user_serializer.data,
            'message': 'Login successful'
        }
        
        if hasattr(user, 'business'):
            business_serializer = BusinessSerializer(user.business)
            response_data['business'] = business_serializer.data
        
        response = Response(response_data, status=status.HTTP_200_OK)
        set_refresh_token_cookie(response, refresh_token, remember_me)
        
        return response
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    refresh_token_str = request.COOKIES.get('refresh_token')
    
    if not refresh_token_str:
        return Response({
            'error': True,
            'message': 'Refresh token not found'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        refresh_token_obj = RefreshToken.objects.get(token=refresh_token_str)
        
        if not refresh_token_obj.is_valid():
            return Response({
                'error': True,
                'message': 'Refresh token is invalid or expired'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        jwt_refresh = JWTRefreshToken(refresh_token_str)
        access_token = str(jwt_refresh.access_token)
        
        user = refresh_token_obj.user
        user.update_activity()
        
        return Response({
            'access_token': access_token
        }, status=status.HTTP_200_OK)
    
    except RefreshToken.DoesNotExist:
        return Response({
            'error': True,
            'message': 'Invalid refresh token'
        }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({
            'error': True,
            'message': 'Token refresh failed'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token_str = request.COOKIES.get('refresh_token')
    
    if refresh_token_str:
        try:
            refresh_token_obj = RefreshToken.objects.get(token=refresh_token_str)
            refresh_token_obj.invalidate()
        except RefreshToken.DoesNotExist:
            pass
    
    response = Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)
    
    clear_refresh_token_cookie(response)
    
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    token_str = request.data.get('token')
    
    if not token_str:
        return Response({
            'error': True,
            'message': 'Token is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        token = EmailVerificationToken.objects.get(token=token_str)
        
        if not token.is_valid():
            return Response({
                'error': True,
                'message': 'Token is invalid or expired'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = token.user
        user.verify_email()
        token.consume()
        
        return Response({
            'message': 'Email verified successfully'
        }, status=status.HTTP_200_OK)
    
    except EmailVerificationToken.DoesNotExist:
        return Response({
            'error': True,
            'message': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@ratelimit(key='user', rate='3/1h', method='POST')
def resend_verification_email(request):
    user = request.user
    
    if user.email_verified:
        return Response({
            'error': True,
            'message': 'Email is already verified'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    verification_token = create_email_verification_token(user)
    send_verification_email(user, verification_token)
    
    return Response({
        'message': 'Verification email sent successfully'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='5/15m', method='POST')
def password_reset_request(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            reset_token = create_password_reset_token(user)
            send_password_reset_email(user, reset_token)
        except User.DoesNotExist:
            pass
        
        return Response({
            'message': 'If an account with that email exists, a password reset link has been sent.'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    serializer = PasswordResetSerializer(data=request.data)
    
    if serializer.is_valid():
        token_str = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            token = PasswordResetToken.objects.get(token=token_str)
            
            if not token.is_valid():
                return Response({
                    'error': True,
                    'message': 'Token is invalid or expired'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = token.user
            user.set_password(new_password)
            user.email_verified = True
            user.save()
            
            RefreshToken.invalidate_all_for_user(user)
            
            token.consume()
            
            return Response({
                'message': 'Password reset successful'
            }, status=status.HTTP_200_OK)
        
        except PasswordResetToken.DoesNotExist:
            return Response({
                'error': True,
                'message': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    user_serializer = UserSerializer(user)
    
    response_data = {
        'user': user_serializer.data
    }
    
    if hasattr(user, 'business'):
        business_serializer = BusinessSerializer(user.business)
        response_data['business'] = business_serializer.data
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = ProfileUpdateSerializer(user, data=request.data, partial=True, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'user': serializer.data,
            'message': 'Profile updated successfully'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        RefreshToken.invalidate_all_for_user(user)
        
        return Response({
            'message': 'Password changed successfully. Please login again.'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
