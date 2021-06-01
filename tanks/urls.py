from django.urls import path, re_path
from tanks import views

urlpatterns = [
    path("", views.index, name="badanie_index"),
    path("delete/<int:id>", views.delete, name="badanie_delete"),
    path("view/<int:id>", views.view, name="badanie_view"),    
    path("tank_edit/", views.tank_edit, name="tank_edit"),    
    path("print/<int:id>", views.myview, name="badanie_print"),

]