"""NewsPaper URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   # адрес, в которое будет перенаправляться пользователь, если он прошел успешно вход на сайт, то есть
   # выходим из приложения sign, с их страниц (также нашей логикой приложения sign сделаем), и перенаправляется в
   # корень нашего сайта (http://127.0.0.1:8000/, так как указаны кавычки), а там уже переходим в файл protect.urls
   # приложения protect и работаем по его адресам, с логикой данного приложения, которую опишем далее в view файле

   path('', include('protect.urls')),

# ___/sign/ будем перенаправляться в файл sign.urls с адресами нашего нового приложения sign, в котором
    # содержится страница аутентификации пользователя и вся логика и проверки с этим связанные, в данном приложении
    # пользователь либо заходит на сайт (проходит идентификацию, аутентификацию и авторизацию), либо создает с нуля
    # свой профиль (то есть регистрируется) и затем заходит. После успешных действий перебрасывается в приложения ниже,
    # данное приложение оно главное, приложение protect, просто для примера

   path('sign/', include('sign.urls')),


   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   # Делаем так, чтобы все адреса из нашего приложения
   # подключались к главному приложению с префиксом products/.
   path('news/', include('news.urls')),
   path('accounts/', include('allauth.urls')),

]