from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    description2 = models.TextField(max_length=150,blank=True,null=True)
    count_villa = models.IntegerField()
    count_bedrooms = models.IntegerField(max_length=1)
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
    project = models.ForeignKey('Project',on_delete=models.CASCADE,blank=True,null=True)
    is_active = models.BooleanField(default=True)


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
    project = models.ForeignKey('Project',on_delete=models.CASCADE,blank=True,null=True)

class PhotoDesign(models.Model):
    photo = models.ImageField(upload_to='photo_design/')

class Archive(models.Model):
    project = models.OneToOneField('Project', on_delete=models.CASCADE)
    archived_on = models.DateTimeField(auto_now_add=True)

