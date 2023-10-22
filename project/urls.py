from django.urls import path, include
from rest_framework import routers
from .views import ProjectViewSet, BedroomViewSet, CharacteristicViewSet, MasterPlanViewSet, PhotoViewSet, TypeViewSet, TypePhotoViewSet, DesignViewSet, PhotoDesignViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'bedrooms', BedroomViewSet)
router.register(r'characteristics', CharacteristicViewSet)
router.register(r'master_plans', MasterPlanViewSet)
router.register(r'photos', PhotoViewSet)
router.register(r'types', TypeViewSet)
router.register(r'type_photos', TypePhotoViewSet)
router.register(r'designs', DesignViewSet)
router.register(r'photo_designs', PhotoDesignViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]
