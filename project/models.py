from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    description = models.TextField()
    count_villa = models.IntegerField()
    count_bedrooms = models.ManyToManyField('Bedroom', blank=True)
    building_area_from = models.IntegerField()
    building_area_to = models.IntegerField()
    land_area_from = models.IntegerField()
    land_area_to = models.IntegerField()
    price_from = models.DecimalField(max_digits=10, decimal_places=2)
    price_to = models.DecimalField(max_digits=10, decimal_places=2)
    characteristic = models.ManyToManyField('Characteristic', blank=True)
    master_plan = models.ManyToManyField('MasterPlan',blank=True)
    video = models.URLField()
    photo = models.ManyToManyField('Photo', blank=True)
    price_list = models.ManyToManyField('PriceList',blank=True,null=True)
    design = models.ManyToManyField('Design',blank=True,null=True)

class Bedroom(models.Model):
    count = models.IntegerField()

class Characteristic(models.Model):
    title = models.CharField(max_length=100)

class MasterPlan(models.Model):
    photo = models.ImageField(upload_to='master_plans/')

class Photo(models.Model):
    photo = models.ImageField(upload_to='photo/')

class PriceList(models.Model):
    ROLE_CHOICES = [
        ('available','Доступно'),
        ('unavailable','Недоступно'),
        ('reserved','Зарезервировано')
    ]
    no = models.CharField(max_length=100)
    type = models.ForeignKey('Type',on_delete=models.CASCADE,blank=True)
    status = models.CharField(max_length=100, choices=ROLE_CHOICES)
    count_bedroom = models.IntegerField()
    land_area = models.IntegerField()
    building_area = models.IntegerField()
    villa = models.IntegerField()
    price = models.IntegerField()
    design = models.ForeignKey('Design',on_delete=models.CASCADE,blank=True)

class Type(models.Model):
    title = models.CharField(max_length=100)
    photo = models.ManyToManyField('TypePhoto', blank=True)

class TypePhoto(models.Model):
    photo = models.ImageField(upload_to='type/')


class Design(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.URLField()
    photo = models.ManyToManyField('PhotoDesign', blank=True)

class PhotoDesign(models.Model):
    photo = models.ImageField(upload_to='photo_design/')