from django.urls import path, re_path
from tanks import views

urlpatterns = [
    path('', views.ZbiornikAll, name='homolog'),
    path('<int:id>', views.ZbiornikId, name='homolog'),
    path('badanie/', views.BadanieTank, name='homolog'),
    path('badanie/<int:id>', views.BadanieTankId, name='homolog'),
    path('badanie/delete/<int:id>', views.BadanieDelete, name='homolog'),
    path('badanie/chart/<int:id>', views.BadanieTankListId, name='homolog'),

    # path('add/', views.HomologAdd, name='homolog_add'),
    # path('update/<str:pk>/', views.HomologUpdate, name='update'),
    # path('detail/<str:pk>/', views.HomologDetail, name='detail'),
    # path('delete/<str:pk>', views.HomologDelete, name='delete'),
    path('szukaj/', views.TankSearch, name='szukaj'),
    path('save/', views.TankAdd, name='save'),
    path('addbadanie/', views.SaveBadanie, name='addBadanie'),
    # path('options/', views.HomologChoise, name='options'),
] 