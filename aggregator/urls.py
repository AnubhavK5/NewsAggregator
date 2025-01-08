from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name = "aggregator-home"),
    path('', views.home, name='news_home'),  # Backend API endpoint for fetching news
    path('search/', views.fetch_news, name='fetch_news'), 
    path('about/', views.about, name='news_about'),  # Backend API endpoint for fetching news
    # path('', views.news_list, name='news_list'),

]