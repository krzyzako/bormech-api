from django import forms  
from .models import Rodzaj  
class RodzajForm(forms.ModelForm):

    class Meta:  
        model = Rodzaj  
        fields = "__all__"  