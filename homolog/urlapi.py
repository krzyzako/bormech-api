from django.urls import path, re_path
from homolog import views

urlpatterns = [
    path('', views.HomologAll, name='homolog'),
    path('<int:id>', views.ViewId, name='id'),
    path('add/', views.HomologAdd, name='homolog_add'),
    path('update/<str:pk>/', views.HomologUpdate, name='update'),
    path('detail/<str:pk>/', views.HomologDetail, name='detail'),
    path('delete/<str:pk>', views.HomologDelete, name='delete'),
    path('szukaj/<str:symbol>', views.HomologBySymbol, name='szukaj'),
    path('options/', views.HomologChoise, name='options'),
] 