from django.urls import path, re_path
from Marketplace_webpage.views import home
from custom_admin.views import user_reports
from newsfeed.views import newsfeed, post_product, profile, edit_profile, logout_view, delete_listing, \
    category_selection, electronics, fashion, garden, sports, edit_listing, report_listing, report_user, search, \
    listing_detail

app_name = 'newsfeed'

urlpatterns = [
    path('', newsfeed, name='newsfeed'),
    path('logout/', logout_view, name='logout'),
    path('post/', post_product, name='post_product'),
    path('profile/', profile, name='profile'),
    path('profile/<pk>/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('delete-listing/<pk>/', delete_listing, name='delete_listing'),
    path('edit_listing/<pk>/', edit_listing, name='edit_listing'),
    path('report_listing/<pk>/', report_listing, name='report_listing'),
    path('listing/<pk>/', listing_detail, name='listing_detail'),
    path('report_user/<pk>/', report_user, name='report_user'),
    path('categories/', category_selection, name='category_selection'),
    path('search/', search, name='search'),
    path('electronics/', electronics, name='electronics'),
    path('fashion/', fashion, name='fashion'),
    path('garden/', garden, name='garden'),
    path('sports/', sports, name='sports'),
    path('user_reports/', user_reports, name='user_reports'),
]