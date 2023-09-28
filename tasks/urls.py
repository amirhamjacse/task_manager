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
         views.TaskListView.as_view(),
         name='home'
         ),
    path('create/task/',
         views.TaskCreateView.as_view(),
         name='task_create'
         ),
    path('details/<int:pk>/task/',
         views.TaskDetailView.as_view(),
         name='task_details'
         ),
    path('update/<int:pk>/task/',
         views.TaskUpdateView.as_view(),
         name='task_update'
         ),
    path('delete/<int:pk>/task/',
         views.TaskDeleteView.as_view(),
         name='task_delete'
         ),
]
