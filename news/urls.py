from django.urls import path
from . import views
from .views import NewsList, NewsDetail

urlpatterns = [
    # path('', views.home, name="home"),
    path('', NewsList.as_view(), name="home"),
    path('detail/<slug:title>', NewsList.as_view(), name="detail"),
]