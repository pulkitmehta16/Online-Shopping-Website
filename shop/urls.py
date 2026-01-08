from django.urls import path
from .import views
urlpatterns = [
    path('', views.index, name='shophome'),
    path('about/', views.about, name='shophome'),
    path('contact/', views.contact, name='shophome'),
    path('tracker/', views.tracker, name='shophome'),
    path('search/', views.search, name='shophome'),
    path('products/<int:myid>', views.prodview, name='shophome'),
    path('checkout/', views.checkout, name='shophome'),
]
