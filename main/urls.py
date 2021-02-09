from django.urls import path

from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category'),
    path('traning-detail/<int:pk>/', TraningDetailView.as_view(), name='detail'),
    path('add-traning/', add_traning, name='add-traning'),
    path('update-traning/<int:pk>/', update_traning, name='update-traning'),
    path('delete-traning/<int:pk>/', DeleteTraningView.as_view(), name='delete-traning'),

]