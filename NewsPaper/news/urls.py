from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, PostDetail, SearchList, PostCreateView, PostUpdateView, PostDeleteView, UserUpdateView, \
   CategoryList, add_subscribe
from django.contrib import admin
from django.urls import path
from django.urls import include

#from .views import IndexView

urlpatterns = [
   #path('', IndexView.as_view()),
   path('', NewsList.as_view()),
   path('<int:pk>/', PostDetail.as_view(), name='post'),
   path('search/', SearchList.as_view()),
   path('create/', PostCreateView.as_view(), name='post_create'),
   path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
   path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
   path('user/', UserUpdateView.as_view(), name='user_update'),
   path('category/', CategoryList.as_view(), name='appointment_post'),
   path('subscribe/<int:pk>', add_subscribe, name='subscribe'),

]