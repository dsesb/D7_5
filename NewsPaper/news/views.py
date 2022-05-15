

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, User, Category, PostCategory
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .filters import NewsFilter
from .forms import PostForm, UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from .tasks import hello, printer


class NewsList(ListView):
    model = Post
    ordering = ['-dateCreation']
    template_name = 'news.html'
    #queryset = Post.objects.order_by('-dateCreation')
    context_object_name = 'news'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class SearchList(ListView):
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    #ordering = 'title'
    template_name = 'search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'search'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    #model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    #context_object_name = 'post'
    #template_name = 'post.html'
    queryset = Post.objects.all()


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'user_update.html'
    form_class = UserForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        return self.request.user


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class CategoryList(ListView):
    model = Category
    template_name = 'appointment_post.html'
    context_object_name = 'category'
    ordering = 'name'
    paginate_by = 10


@login_required
def add_subscribe(request, pk):
    a = request.user
    a.save()
    b = Category.objects.get(id=pk)
    b.subscribers.add(a)
    return redirect('/news/')


@receiver(m2m_changed, sender=PostCategory)
def post(sender, instance, *args, **kwargs):
    for cat_id in instance.postCategory.all():
        print(cat_id)
        users = Category.objects.filter(name=cat_id).values("subscribers")
        link = ''.join(['http://', get_current_site(None).domain, ':8000/news/'])
        for user_id in users:
            send_mail(
                subject=f"{instance.title}",
                message=f"Здравствуй, {User.objects.get(pk=user_id['subscribers']).username}."
                        f" Новая статья в твоём любимом разделе! \n {instance.text[:50]} \n"
                        f" Перейдите {link} чтобы прочесть статью.",
                from_email='vas3011ds@yandex.ru',
                recipient_list=[User.objects.get(pk=user_id['subscribers']).email]
            )


#class IndexView(View):

#    def get(self, request):
#        printer.delay(1)
#        return HttpResponse('Hello!')

#def get(self, request):
#    printer.delay(1)
#    return HttpResponse('Hello!')












