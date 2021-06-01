from django.db import models
from homolog.models import Rodzaj
class Zbiornik(models.Model):
    typ_pekniecia = (
        (0, 'empty'),
        (1, 'plastyczne'),
        (2, 'kruche'),
    )
    numer = models.CharField(max_length=4)
    rodzaj = models.ForeignKey(Rodzaj, related_name='tracks', on_delete=models.CASCADE)
    dataBadania = models.DateField(auto_now=False, default='2020-01-01')
    nr_odbioru = models.IntegerField(default=1)
    nr_rozrywania = models.IntegerField(default=1)
    pekniecie = models.IntegerField(choices=typ_pekniecia, default=0)
    def __str__(self):
        return self.rodzaj.symbol +' '+self.numer
    class Meta:
        verbose_name = 'Zbiornik'
        verbose_name_plural = 'Zbiorniki'

class Badanie(models.Model):
    zbiornik = models.ForeignKey("Zbiornik", on_delete=models.CASCADE)
    woda = models.FloatField()
    cisnienie = models.IntegerField()
    czas = models.TimeField(auto_now=False)
    def __str__(self):
        return  str(self.id)+' --> '+self.zbiornik.rodzaj.symbol +' '+ self.zbiornik.numer +' przyrost : ' + str(self.woda) +' ciśnienie : '+ str(self.cisnienie)

    class Meta:
        verbose_name = 'Badanie'
        verbose_name_plural = 'Badania'