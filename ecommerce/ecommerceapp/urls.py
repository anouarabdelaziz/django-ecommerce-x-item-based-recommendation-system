from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.userlogout, name='logout'),
    path('register/', views.register, name='register'),
    path('checkout/', views.checkout, name='checkout'),
    path('updated_item/', views.updateditem),
    path('cart/<int:id>/', views.cart, name='cart'),

]

