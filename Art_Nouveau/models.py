from django.db import models
'''
class CategorieProdus(models.Model):
    nume = models.CharField(max_length=64)
    descriere = models.TextField(max_length=256)
    icon_url = models.URLField()

class TipProdus(models.Model):
    tipuri = {
        'PICTURA': 'Pictura',
        'SCULPTURA': 'Sculptura',
        'DESEN': 'Desen',
        'FOTOGRAFIE': 'Fotografie',
        'DIGITAL': 'ArtA digitala',
    }
    tip = models.CharField(choices=tipuri)
    descriere = models.TextField(max_length=512)
    fizic = models.BooleanField()

class Produs(models.Model):
    cat_produs = models.ForeignKey(CategorieProdus)
    tip_produs = models.ForeignKey(TipProdus)
    nume = models.CharField(max_length=128)
    pret = models.FloatField()
    stoc = models.PositiveIntegerField()
    descriere = models.TextField(max_length=1024)
    
'''
