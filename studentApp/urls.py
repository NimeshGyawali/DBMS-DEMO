from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('add-staff-member/', views.add_staff_member, name='add_staff_member'),
    path('add-student/', views.add_student, name='add_student'),
    path('add-course/', views.add_course, name='add_course'),
    path('add-project/', views.add_project, name='add_project'),
    path('add-exam/', views.add_exam, name='add_exam'),
    path('add-enrollment/', views.add_enrollment, name='add_enrollment'),
    path('add-teaching/', views.add_teaching, name='add_teaching'),
    path('search-results/', views.search_results, name='search_results'),
]
