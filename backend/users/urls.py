from django.urls import include, path,re_path
from rest_framework import routers
from . import views
from rest_auth.registration.views import VerifyEmailView, RegisterView

router = routers.DefaultRouter()
router.register(r'property', views.PropertyView)
router.register(r'applicant',views.ApplicantView)
router.register(r'tenant',views.TenantView)
router.register(r'landlord', views.LandLordView)

urlpatterns = [
    path('', include(router.urls)),
    path('rest-auth/', include('rest_auth.urls')),
    path('registration/', views.CustomRegisterView.as_view(),name="custom-registration"),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
     name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
     name='account_confirm_email'),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]