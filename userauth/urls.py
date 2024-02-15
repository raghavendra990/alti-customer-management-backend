from django.conf.urls import include
from django.urls import path

from .views import LoginAPIView, RegisterAPIView, LogoutAPIView, UserDetailsAPIView, PlanView, RenewPlan, UpgradeDowngradePlan

auth_enpoints = [
    path('login',  LoginAPIView.as_view(), name="login"),
    path('register',  RegisterAPIView.as_view(), name="register"),
    path('logout',  LogoutAPIView.as_view(), name="logout"),
    path('profile',  UserDetailsAPIView.as_view(), name="profile"),
    path('plan',  PlanView.as_view(), name="plan"),
    path('renewPlan',  RenewPlan.as_view(), name="plan"),
    path('upgradeDowngradePlan',  UpgradeDowngradePlan.as_view(), name="plan"),


]

urlpatterns = [
    path('userauth/', include(auth_enpoints))
]