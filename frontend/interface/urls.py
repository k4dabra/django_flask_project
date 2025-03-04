from django.urls import path
from . import views

urlpatterns = [
    path('',views.main),
    path('readPage/',views.read_page),
    path('addPage/',views.add_page),
    path('read/',views.read),
    path('add/',views.add),
]
