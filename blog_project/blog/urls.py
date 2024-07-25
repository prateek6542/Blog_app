from django.urls import path
from . import views
from .views import sign_up, custom_logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:id>/', views.blog_detail, name='blog_detail'),
    path('search/', views.blog_search, name='blog_search'),
    path('signup/', sign_up, name='sign_up'),
    path('share/<int:blog_id>/', views.blog_share, name='blog_share'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
