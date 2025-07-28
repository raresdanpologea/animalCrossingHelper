from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_grid, name='item_grid'),
]
