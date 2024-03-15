from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('add/', views.add_student, name='add_student'),
    path('search/', views.search_student, name='search_student'),
]
