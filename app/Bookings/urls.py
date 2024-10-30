from django.urls import path
from .views import hotel_list, hotel_detail, book_hotel

urlpatterns = [
    path('hotels/', hotel_list, name='hotel_list'),
    path('hotels/<int:pk>/', hotel_detail, name='hotel_detail'),
    path('hotels/<int:hotel_id>/book/', book_hotel, name='book_hotel'),
]