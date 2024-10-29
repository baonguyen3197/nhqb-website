from django.urls import path
from .views import airport_list

urlpatterns = [
    path('list/', airport_list, name='airport_list'),
]