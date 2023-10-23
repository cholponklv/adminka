from django.urls import path, include
from rest_framework import routers
from .views import ProjectViewSet, CharacteristicViewSet, MasterPlanViewSet, PhotoViewSet, TypeViewSet, TypePhotoViewSet, DesignViewSet, PhotoDesignViewSet,PriceListViewSet
from . import views 
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'characteristics', CharacteristicViewSet)
router.register(r'master_plans', MasterPlanViewSet)
router.register(r'photos', PhotoViewSet)
router.register(r'types', TypeViewSet)
router.register(r'type_photos', TypePhotoViewSet)
router.register(r'designs', DesignViewSet)
router.register(r'photo_designs', PhotoDesignViewSet)
router.register(r'price_lists', PriceListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:pk>/price_lists/<int:price_list_pk>/', views.ProjectViewSet.as_view({'get': 'price_list_detail'}), name='project-price-list-detail'),
    path('projects/<int:pk>/price_lists/<int:price_list_pk>/hide_price_lists/', ProjectViewSet.as_view({'post': 'hide_price_list'}), name='project-hide-price-list'),
    path('projects/<int:pk>/price_lists/<int:price_list_pk>/delete/', ProjectViewSet.as_view({'delete': 'delete_price_list'}), name='project-delete-price-list'),
    path('projects/<int:pk>/price_lists/<int:price_list_pk>/copy/', ProjectViewSet.as_view({'post': 'copy_price_list'}), name='project-copy-price-list'),
    path('projects/<int:pk>/design/<int:design_pk>/', ProjectViewSet.as_view({'get': 'view_design_detail'}), name='project-view-design'),
    path('projects/<int:pk>/designs/<int:design_pk>/update/', ProjectViewSet.as_view({'put': 'update_design'}), name='project-update-design'),
    path('projects/<int:pk>/designs/<int:design_pk>/delete/', ProjectViewSet.as_view({'delete': 'delete_design'}), name='project-delete-design'),
    path('projects/<int:pk>/price_lists/<int:price_list_pk>/update/', ProjectViewSet.as_view({'put': 'update_price_list'}), name='project-update-price-list'),


]

