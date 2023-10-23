from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'add_staff', viewset = views.AddStaffUserViewSet, basename='add_staff')

urlpatterns = [
    path('', include(router.urls)),
    path('change_password/',views.ChangePasswordView.as_view(), name='change_password'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ####
    path('recover_send_mail/', views.SendTokenToRecoverView.as_view(), name = 'recover_email'),
    path('check_recover_token/', views.CheckRecoverTokenView.as_view(), name = 'check_recover_token'),
    path('new_password_recover/', views.OldUserToNew.as_view(), name = 'new_password_recover'),
    ###

]