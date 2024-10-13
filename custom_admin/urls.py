from django.urls import path

from newsfeed.views import profile
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.users, name='users'),
    path('delete_user/<pk>/', views.delete_user, name='delete_user'),
    path('messages/', views.contact_messages, name='messages'),
    path('products/', views.products, name='products'),
    path('delete_product/<pk>/', views.delete_product, name='delete_product'),
    path('listing_reports/', views.listing_reports, name='listing_reports'),
    path('user_reports/', views.user_reports, name='user_reports'),
    path('delete_listing_report/<pk>/', views.delete_listing_report, name='delete_listing_report'),
    path('delete_message/<pk>/', views.delete_message, name='delete_message'),
    path('delete_user_report/<pk>/', views.delete_user_report, name='delete_user_report'),
]