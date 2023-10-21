from django.contrib import admin
from .models import Project, Bedroom, Characteristic, MasterPlan, Photo, PriceList, Type, TypePhoto, Design, PhotoDesign

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'description')  
    search_fields = ('title', 'description')  
class PriceListAdmin(admin.ModelAdmin):
    list_filter = ('status',)  
    list_display = ('no', 'type', 'status', 'count_bedroom', 'land_area', 'building_area', 'villa', 'price')  # Отображение полей в списке

# Регистрация моделей с настройками административного интерфейса
admin.site.register(Project, ProjectAdmin)
admin.site.register(Bedroom)
admin.site.register(Characteristic)
admin.site.register(MasterPlan)
admin.site.register(Photo)
admin.site.register(PriceList, PriceListAdmin)
admin.site.register(Type)
admin.site.register(TypePhoto)
admin.site.register(Design)
admin.site.register(PhotoDesign)
