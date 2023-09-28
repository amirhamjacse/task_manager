from django.urls import path
from tasks import views

urlpatterns = [
    path('register/',
         views.RegistrationView.as_view(),
         name='register'
         ),
    path('accounts/login/',
         views.LoginView.as_view(),
         name='login'
         ),
    path('logout/',
         views.LogoutView.as_view(),
         name='logout'
         ),
    path('',
         views.HomeView.as_view(),
         name='home'
         ),
]
