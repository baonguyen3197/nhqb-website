from django.urls import path
from .views import hotel_list, hotel_detail, book_hotel_step1, book_hotel_step2, book_hotel_step3, book_hotel_step4

urlpatterns = [
    path('hotels/', hotel_list, name='hotel_list'),
    path('hotels/<int:pk>/', hotel_detail, name='hotel_detail'),
    path('book/step1/', book_hotel_step1, name='book_hotel_step1'),
    path('book/step2/', book_hotel_step2, name='book_hotel_step2'),
    path('book/step3/', book_hotel_step3, name='book_hotel_step3'),
    path('book/step4/', book_hotel_step4, name='book_hotel_step4'),
]