from django.db import models
import datetime
# Create your models here.
class Rodzaj(models.Model):
    typ = (
        (1, 'Teroidalny wewnętrzny'),
        (2, 'Teroidalny zewnętrzny'),
        (3, 'Teroidalny zewnętrzny pełny'),
        (4, 'Walcowy'),
        )
        
    tank = models.IntegerField(choices=typ, default=1)
    symbol = models.CharField(max_length=8,unique=True)
    height = models.IntegerField(verbose_name="Wysokość",blank=True,null=True)
    capacity = models.IntegerField(verbose_name="Pojemność")
    dimeter = models.IntegerField(verbose_name="Średnica")
    approval = models.CharField(max_length=16, verbose_name="Homologacja")
    weight = models.FloatField(verbose_name="Waga",blank=True,null=True)
    
    def __str__(self):
            return  self.symbol
    class Meta:
        
        verbose_name = 'Rodzaj'
        verbose_name_plural = 'Rodzaje'


