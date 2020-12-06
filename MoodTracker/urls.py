from django.urls import path
from . import views


urlpatterns = [
    path('', views.Index.as_view()),
    path('dashboard/', views.Dashboard.as_view(),),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout),
    path('new_entry/', views.NewEntry.as_view()),
    path('entries/', views.Entries.as_view()),
    path('radio/', views.Radio.as_view()),
    path('entry_replier/<int:reply_id>/', views.Replier.as_view(), name='reply_id'),
]