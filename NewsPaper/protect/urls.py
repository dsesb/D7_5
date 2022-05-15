from django.urls import path
from .views import IndexView

urlpatterns = [
    #перенаправляемся на единственное представление IndexView
    path('', IndexView.as_view()),
]