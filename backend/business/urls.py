from django.urls import path
from . import views

urlpatterns = [
    path('setup/', views.setup_business, name='setup_business'),
    path('me/', views.get_business, name='get_business'),
    path('update/', views.update_business, name='update_business'),
]
