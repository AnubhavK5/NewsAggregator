from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name = "aggregator-home"),
    path('', views.fetch_news, name='news_homepage'),  # Backend API endpoint for fetching news
    path('about/', views.about, name='news_about'),  # Backend API endpoint for fetching news
    # path('', views.news_list, name='news_list'),

]