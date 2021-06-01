from django.db import models

# Create your models here.
class Mqtt(models.Model):
    test1 = models.CharField(max_length=50)
    trest2 = models.CharField(max_length=50)
    def __str__(self):
        return self.test1

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Mqtt'
        verbose_name_plural = 'Mqtt'