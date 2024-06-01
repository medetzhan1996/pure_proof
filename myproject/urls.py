from django.urls import path
from .views import *

app_name = 'myproject'

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('search/', ProductSearchView.as_view(), name='search_product'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('check-product/', CheckProductView.as_view(), name='check_product'),

    path('', IndexListView.as_view(), name='index'),
    path('blog/list', BlogListView.as_view(), name='blog_list'),
    path('chat/', chat, name='chat'),

    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    path('profile/update/', profile_view, name='profile_view'),
    path('register/', register, name='register'),

]
