from django.urls import path
from . import views


urlpatterns = [
    path('', views.Index.as_view()),
    path('dashboard/', views.Dashboard.as_view(),),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout)
]