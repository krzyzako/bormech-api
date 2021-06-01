
from django.urls import path, re_path
from homolog import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('add', views.add, name="addhomolog"),  
    path('edit/<int:id>', views.edit , name="homolog/edit/"),
    path('update/<int:id>', views.update, name="homolog/update/"),  
    path('delete/<int:id>', views.delete, name="homolog/delete/"), 
    path('widgets/', views.testy, name='test'),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

] 